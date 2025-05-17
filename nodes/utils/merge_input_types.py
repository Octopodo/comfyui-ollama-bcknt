def merge_input_types(inputTypes: list) -> dict:
    """
    Merges a list of input types into a single type.
    """
    if len(inputTypes) == 1:
        return inputTypes[0]
    
    mergedTypes = {"required": {}, "optional": {}}
    
    for inputType in inputTypes:
        if "required" in inputType:
            mergedTypes["required"].update(inputType["required"])
        if "optional" in inputType:
            mergedTypes["optional"].update(inputType["optional"])
    
    return mergedTypes