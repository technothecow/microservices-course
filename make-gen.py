import os
import subprocess
import sys
import re
from pathlib import Path

def fix_imports(file_path, package_name):
    """Fix imports in generated protobuf files to use relative imports."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace direct imports with relative imports
    fixed_content = re.sub(
        r'import (\w+_pb2) as', 
        r'from . import \1 as', 
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(fixed_content)

def main():
    # Find all microservice directories that start with 'sn-'
    microservices = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith('sn-')]
    
    # First, run make-gen in all services where it's present
    for service in microservices:
        make_gen_path = os.path.join(service, 'make-gen.py')
        if os.path.exists(make_gen_path):
            print(f'Found make-gen.py in {service}, running it...')
            try:
                # Change to the service directory and run make-gen
                cwd = os.getcwd()
                os.chdir(service)
                subprocess.run(['python', '-m', 'make-gen'], check=True)
                os.chdir(cwd)  # Return to original directory
            except subprocess.CalledProcessError as e:
                print(f'  Error running make-gen in {service}: {e}', file=sys.stderr)
    
    # Continue with the original proto generation logic
    for source_service in microservices:
        proto_path = os.path.join(source_service, 'docs/proto/service.proto')
        
        # Check if the proto file exists
        if os.path.exists(proto_path):
            print(f'Found proto in {source_service}, generating code for other services...')
            
            # Generate code for all other microservices
            for target_service in microservices:
                # Create output directory
                package_name = source_service.replace('-', '_')
                output_dir = os.path.join(target_service, f'src/proto/{package_name}')
                os.makedirs(output_dir, exist_ok=True)
                
                print(f'  Generating proto code from {source_service} to {target_service}...')
                
                try:
                    # Run protoc compiler without the unsupported options
                    subprocess.run([
                        'python', '-m', 'grpc_tools.protoc',
                        f'--proto_path={os.path.join(source_service, "docs/proto")}',
                        f'--python_out={output_dir}',
                        f'--grpc_python_out={output_dir}',
                        'service.proto'
                    ], check=True)
                    
                    # Fix imports in all the generated files
                    pb2_file = os.path.join(output_dir, 'service_pb2.py')
                    grpc_file = os.path.join(output_dir, 'service_pb2_grpc.py')
                    
                    if os.path.exists(pb2_file):
                        # Create an empty __init__.py file
                        with open(os.path.join(output_dir, '__init__.py'), 'w') as f:
                            pass
                    
                    if os.path.exists(grpc_file):
                        fix_imports(grpc_file, package_name)
                        
                except subprocess.CalledProcessError as e:
                    print(f'  Error generating code: {e}', file=sys.stderr)

if __name__ == '__main__':
    main()