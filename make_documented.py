import sys

sys.path.insert(0, "multidoc")

from multidoc.generate import generate_pybind_documented, generate_cpp_documented

if __name__ == "__main__":
    generate_pybind_documented(api_prefix="docstrings", target_src="../tudatpy")
    generate_cpp_documented(api_prefix="docstrings", target_src="../tudat")
