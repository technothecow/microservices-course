import os
import ast

def find_servicer_class():
    """Find the file containing UserServiceServicer class in src directory."""
    service_dir = "src"
    
    if not os.path.exists(service_dir):
        print(f"Directory {service_dir} does not exist.")
        return None, None
    
    for root, _, files in os.walk(service_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if "class UserServiceServicer" in content:
                            tree = ast.parse(content)
                            return file_path, tree
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return None, None

def extract_methods(tree):
    """Extract methods from UserServiceServicer class."""
    methods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'UserServiceServicer':
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith('__'):
                    methods.append(item.name)
    return methods

def generate_procedure_files(methods):
    """Generate Python files for each method in src/procedures directory."""
    procedures_dir = "src/procedures"
    os.makedirs(procedures_dir, exist_ok=True)
    
    created_files = []
    skipped_files = []
    
    for method in methods:
        file_path = os.path.join(procedures_dir, f"{method}.py")
        
        # Skip if file already exists
        if os.path.exists(file_path):
            skipped_files.append(method)
            continue
            
        file_content = f"""def {method}(request, context):
    \"\"\"
    Implementation of {method} procedure.
    \"\"\"
    # TODO: Implement {method} procedure
    pass
"""
        
        with open(file_path, 'w') as file:
            file.write(file_content)
        created_files.append(method)
    
    # Generate __init__.py with all methods regardless of whether they were created or skipped
    init_content = ""
    for method in methods:
        init_content += f"from .{method} import {method}\n"
    
    with open(os.path.join(procedures_dir, "__init__.py"), 'w') as file:
        file.write(init_content)
        
    return created_files, skipped_files

def main():
    file_path, tree = find_servicer_class()
    
    if not file_path:
        print("UserServiceServicer class not found in src directory.")
        return
    
    print(f"Found UserServiceServicer in {file_path}")
    
    methods = extract_methods(tree)
    if not methods:
        print("No methods found in UserServiceServicer class.")
        return
    
    created_files, skipped_files = generate_procedure_files(methods)
    
    print(f"Generated {len(created_files)} new procedure files")
    if created_files:
        print(f"Created: {', '.join(created_files)}")
    if skipped_files:
        print(f"Skipped existing files: {', '.join(skipped_files)}")
    print(f"Updated __init__.py with {len(methods)} methods")

if __name__ == "__main__":
    main()
