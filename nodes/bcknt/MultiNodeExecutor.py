from typing import List, Dict, Any, Type, Union, Tuple

class MultiNodeExecutor:
    def __init__(self, node_configs: List[Dict[str, Any]]):
        """
        Inicializa el ejecutor de nodos.

        :param node_configs: Lista de configuraciones de nodos. Cada configuración debe incluir:
            - 'node': La clase del nodo (requerido).
            - 'fixed_kwargs': Diccionario de argumentos fijos (opcional, por defecto {}).
            - 'inputs': Dependencias o inyecciones directas. Puede ser:
                - Una tupla: (node_alias, param_name) para una dependencia única.
                - Una lista de tuplas: [(node_alias, param_name)] para múltiples dependencias.
                - Un diccionario: {'param_name': value} para inyección directa.
            - 'alias': Alias opcional del nodo (por defecto: nombre de la clase o nombre con índice).
        """
        self.node_configs = []
        alias_counter = {}  # Contador para nombres de clase duplicados
        alias_to_class = {}  # Mapeo de alias a clase

        for config in node_configs:
            cls = config['node']
            alias = config.get('alias')

            if alias:
                if alias in alias_to_class:
                    raise ValueError(f"Alias duplicado '{alias}' proporcionado.")
                alias_to_class[alias] = cls
            else:
                base_name = cls.__name__
                alias_counter[base_name] = alias_counter.get(base_name, 0) + 1
                alias = base_name if alias_counter[base_name] == 1 else f"{base_name}_{alias_counter[base_name]}"
                while alias in alias_to_class:  # Asegurar unicidad
                    alias_counter[base_name] += 1
                    alias = f"{base_name}_{alias_counter[base_name]}"
                alias_to_class[alias] = cls

            config_copy = config.copy()
            config_copy['alias'] = alias
            self.node_configs.append(config_copy)

        self.alias_to_class = alias_to_class
        self.results = {}
        self.instances = {}

    @staticmethod
    def remove_inputs(input_data: Dict[str, Any], input_names: List[str]) -> Dict[str, Any]:
        """
        Removes specified inputs from the input dictionary.

        :param input_data: The input dictionary.
        :param input_names: List of input names to remove.
        :return: The modified input dictionary.
        """
        if 'required' in input_data:
            for name in input_names:
                input_data['required'].pop(name, None)
        if 'optional' in input_data:
            for name in input_names:
                input_data['optional'].pop(name, None)
        return input_data

    def _get_node_params(self, node_class: Type) -> Dict[str, Any]:
        """
        Obtiene los parámetros requeridos y opcionales del nodo basados en INPUT_TYPES.

        :param node_class: La clase del nodo.
        :return: Diccionario con parámetros 'required' y 'optional'.
        """
        input_types = node_class.INPUT_TYPES()
        return {
            'required': input_types.get('required', {}),
            'optional': input_types.get('optional', {})
        }

    def _prepare_node_kwargs(self, node_class: Type, global_kwargs: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara los argumentos clave para el nodo.

        :param node_class: La clase del nodo.
        :param global_kwargs: Argumentos clave globales.
        :param config: La configuración del nodo.
        :return: Diccionario de argumentos clave para el nodo.
        """
        params = self._get_node_params(node_class)
        required_params = set(params['required'].keys())
        optional_params = set(params['optional'].keys())

        # Inicializar con valores por defecto para parámetros opcionales
        node_kwargs = {
            k: v[1]['default']
            for k, v in params['optional'].items()
            if 'default' in v[1]
        }

        # Añadir global_kwargs para parámetros válidos
        for k in required_params | optional_params:
            if k in global_kwargs:
                node_kwargs[k] = global_kwargs[k]

        # Procesar inputs
        inputs = config.get('inputs', [])
        if isinstance(inputs, dict):
            # Inyección directa
            for param, value in inputs.items():
                if not isinstance(value, tuple):
                    value = (value,)  # Convertir a tupla si no lo es
                if param in required_params | optional_params:
                    node_kwargs[param] = value
                else:
                    raise ValueError(f"Parámetro '{param}' no válido para {node_class.__name__}")
        else:
            # Dependencias
            dependencies = [inputs] if isinstance(inputs, tuple) else inputs
            self._process_dependencies(node_class, dependencies, node_kwargs, required_params, optional_params)

        # Añadir fixed_kwargs
        fixed_kwargs = config.get('fixed_kwargs', {})
        node_kwargs.update(fixed_kwargs)

        return node_kwargs

    def _process_dependencies(self, node_class: Type, dependencies: List[Tuple[str, Union[str, List[Tuple[str, str]]]]], node_kwargs: Dict[str, Any], required_params: set, optional_params: set):
        """
        Procesa las dependencias y añade los valores correspondientes a node_kwargs.

        :param node_class: La clase del nodo.
        :param dependencies: Lista de dependencias.
        :param node_kwargs: Diccionario a actualizar con valores de dependencias.
        :param required_params: Conjunto de nombres de parámetros requeridos.
        :param optional_params: Conjunto de nombres de parámetros opcionales.
        """
        for dep in dependencies:
            if len(dep) != 2:
                raise ValueError(f"Formato inválido en inputs para {node_class.__name__}: {dep}")
            dep_node, dep_spec = dep  # dep_node es el alias

            if dep_node not in self.results:
                raise ValueError(f"Dependencia {dep_node} no encontrada para {node_class.__name__}")

            # Obtener la clase del nodo dependiente
            dep_class = self.alias_to_class[dep_node]

            # Obtener RETURN_NAMES del nodo dependiente
            return_names = getattr(dep_class, 'RETURN_NAMES', None)
            if return_names is None:
                raise ValueError(f"El nodo {dep_node} no tiene RETURN_NAMES definido")

            # Obtener el resultado del nodo dependiente
            dep_result = self.results[dep_node]

            if isinstance(dep_spec, str):
                # Caso 1: Coincidencia automática de nombres
                if dep_spec in return_names:
                    index = return_names.index(dep_spec)
                    if dep_spec in required_params | optional_params:
                        node_kwargs[dep_spec] = dep_result[index]
                    else:
                        raise ValueError(f"Input '{dep_spec}' no válido para {node_class.__name__}")
                else:
                    raise ValueError(f"'{dep_spec}' no encontrado en RETURN_NAMES de {dep_node}")
            elif isinstance(dep_spec, list):
                # Caso 2: Mapeo explícito
                for out_name, in_name in dep_spec:
                    if out_name in return_names:
                        index = return_names.index(out_name)
                        if in_name in required_params | optional_params:
                            node_kwargs[in_name] = dep_result[index]
                        else:
                            raise ValueError(f"Input '{in_name}' no válido para {node_class.__name__}")
                    else:
                        raise ValueError(f"'{out_name}' no encontrado en RETURN_NAMES de {dep_node}")
            else:
                raise ValueError(f"Especificación de dependencia inválida para {dep_node}: {dep_spec}")

    def _execute_node(self, node_class: Type, node_kwargs: Dict[str, Any], alias: str) -> Any:
        """
        Ejecuta el método del nodo con los argumentos clave proporcionados.

        :param node_class: La clase del nodo.
        :param node_kwargs: Argumentos clave para el método del nodo.
        :param alias: El alias del nodo.
        :return: El resultado de la ejecución del nodo.
        """
        # Obtener el nombre del método de ejecución (por defecto 'execute')
        function_name = getattr(node_class, 'FUNCTION', 'execute')

        # Obtener o crear la instancia del nodo
        if alias not in self.instances:
            self.instances[alias] = node_class()
        node_instance = self.instances[alias]

        # Obtener el método del nodo
        node_method = getattr(node_instance, function_name)

        # Obtener parámetros requeridos y opcionales
        params = self._get_node_params(node_class)
        required_params = set(params['required'].keys())
        optional_params = set(params['optional'].keys())

        # Verificar parámetros requeridos faltantes
        missing_params = required_params - set(node_kwargs.keys())
        if missing_params:
            raise ValueError(f"Faltan parámetros requeridos para {alias}: {missing_params}")

        # Ajustar node_kwargs: extraer el primer elemento de las tuplas para parámetros que no son listas/tuplas en INPUT_TYPES
        adjusted_kwargs = {}
        for param, value in node_kwargs.items():
            param_info = params['required'].get(param, params['optional'].get(param))
            if param_info:
                expected_type = param_info[0]  # Tipo esperado según INPUT_TYPES
                # Si el valor es una tupla y el tipo esperado no es una lista o tupla, extraer el primer elemento
                if isinstance(value, tuple) and not isinstance(expected_type, (list, tuple)):
                    adjusted_kwargs[param] = value[0]
                else:
                    adjusted_kwargs[param] = value
            else:
                adjusted_kwargs[param] = value  # Mantener el valor original si no hay info de tipo

        # Ejecutar el método con los argumentos ajustados
        return node_method(**adjusted_kwargs)

    def execute_nodes(self, **global_kwargs) -> Dict[str, Any]:
        """
        Ejecuta todos los nodos y devuelve un diccionario con los resultados.

        :param global_kwargs: Argumentos clave globales disponibles para todos los nodos.
        :return: Diccionario con los resultados de cada nodo, usando el alias como clave.
        """
        self.results = {}
        self.instances = {}

        for config in self.node_configs:
            node_class = config['node']
            alias = config['alias']
            node_kwargs = self._prepare_node_kwargs(node_class, global_kwargs, config)
            result = self._execute_node(node_class, node_kwargs, alias)
            self.results[alias] = result

        return self.results