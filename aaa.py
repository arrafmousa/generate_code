import ast
import builtins


class APIDetector(ast.NodeVisitor):
    def __init__(self, source_code):
        self.source_code = source_code
        self.api_calls = []

    def visit_Call(self, node):
        # Get the function/API name
        func_name = ast.get_source_segment(self.source_code, node.func)

        # Get the arguments of the function/API call
        args = [ast.get_source_segment(self.source_code, a) for a in node.args]

        # Construct a dictionary of the function/API name and its arguments
        self.api_calls.append({
            "api": func_name,
            "args": args
        })
        self.generic_visit(node)  # Continue visiting child nodes


def parse_API(code):
    # Parse the code and detect built-in API calls and their arguments
    detector = APIDetector(code)
    detector.visit(ast.parse(code))

    # Process the source code to embed the API and ARG tags
    for call in detector.api_calls:
        api_name = call["api"]
        args = call["args"]
        args_with_tags = ', '.join([f'<ARG>{arg}</ARG>' for arg in args])

        # Replace the original call with the tagged version
        original_call = f"{api_name}({', '.join(args)})"
        tagged_call = f"<API>{api_name}</API>({args_with_tags})"
        code = code.replace(original_call, tagged_call)  # Replace only the first occurrence
    return code