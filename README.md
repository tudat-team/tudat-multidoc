# ``tudat-multidoc``

This repository contains the docstring source for the ``tudat``/``tudatpy``  
repository. This repository effectively contains a description of the Tudat 
API. To understand the content of this file, the reader should be familiar
with the structure and content of the `tudat-bundle`, which is explained in the
`tudat-bundle/README.md` (one level higher than the directory where the current
README is located). If you want to know how to write API documentation, please
make sure to read the README file located in the lower-level `tudat-multidoc/docstring` 
directory.

## Structure of `tudat-multidoc`

In the `tudat-multidoc` directory, there are two subdirectories:
1. `tudat-multidoc/docstrings`, where the documentation is actually written in YAML files (this constitues the "source" 
   of the API system). Instructions on how to write the docstrings and on the structure of such directory
   are provided in the dedicated `docstrings/README.md` file.
2. `tudat-multidoc/multidoc`, where the software to build the API is located. The content of this repository
   should not be modified. 
   
## Branches

The branches used to write the documentation are the following (listed for each repo):

- `tudat-bundle`: main
- `tudat`: develop
- `tudatpy`: develop
- `tudat-multidoc`: main
- `tudat-multidoc/multidoc`: develop

If you are writing the API for a specific module/project, you are recommended to create a new branch and then open a pull request.

## How to generate documented versions of `tudat`/`tudatpy` 

This procedure exists as an additional procedure to the [tudat-bundle](https://github.com/tudat-team/tudat-bundle)
setup procedure, for those who are working with modifying the Tudat API 
documentation. **The following is only valid when this repository is a 
submodule of the `tudat-bundle` for developers**.

1. Install the `tudat-multidoc` conda environment:

```bash
conda env create -f environment.yaml
```

2. Activate the `tudat-multidoc` environment:

```bash
conda activate tudat-multidoc
```

3. Generate the documented versions of `tudat` and `tudatpy` through the
   Command Line Interface (CLI) for Python. This is explained in more detail below.

### Bundle CLI

A set of command-line interface tools have been made to abstract the tedious tasks surrounding the `tudat-bundle`.

The `cli` command must be executed
1. with your `tudat-multidoc` environment activated and
2. inside a directory containing the `.multidoc.cfg` file (e.g., in the `tudat-bundle` directory).

This file provides all of the configurable arguments for the `cli` tool. The variables are fairly straightforward.

> **PLEASE NOTE**: Ensure (1) current working directory is `tudat-bundle`, (2) a `cli` directory is present in your version of the `tudat-bundle` and (3) a `.multidoc.cfg` file exists in root of `tudat-bundle`.

Below gives four different commands that you will be using in your workflow.

```bash
# the scope of this tool
python cli d    # document   [1]
python cli b    # build      [2]
python cli s    # sphinx     [3]
python cli a    # all        [*]
```

The subcommands, their scopes and **their required order of execution** are summarised by the following:

1. **`[document/d]`** Generating documented versions of project sources.
2. **`[build/b]`** Building the `tudat-bundle` and its contained project sources.
3. **`[sphinx/s]`** Building the `sphinx` API documentation for the **builds** of the `tudat-bundle` subprojects.
4. **`[all/a]`** Executes 1,2 and 3 in that order.

TODO: the following is currently not working.

It is possible to build only one project (either `tudat` or `tudatpy`) by appending `-p project_name` to the `python cli X`
command, where `project_name` is `tudat` or `tudatpy` and `X` is one of the four letters listed above.

#### 1. Documenting

After running `python cli d`, the following directories will appear in your `tudat-bundle`
directory:

- `tudat-bundle/.tudat-documented`
- `tudat-bundle/.tudatpy-documented`

They are listed under `tudat-bundle/.gitignore`, so they will
not be tracked. These repositories are essential copies of the original tudat and tudatpy repositories,
with the addition of the docstrings (see below). These two repos will constitute the source from which the 
build of both tudat and tudatpy will be done.

> **PLEASE NOTE**: These two repos will be overwritten every time the `python cli d` command 
> is executed. Therefore, if you want to make long-lasting changes to the project source code, do NOT
> do it in these folders, but in the original directories, then re-run the documenting command.


This is what happens in this step: the docstrings located in the 
`tudat-multidoc/docstrings` directory are parsed, validated, formatted (currently, in NumPy style) and
placed in a C++ function. This is located in:

- `.tudat-documented/include/tudat/docstrings.h` for tudat
- `.tudatpy-documented/include/tudatpy/docstrings.h` for tudatpy

This function will be used during the next step (the build step) to link each docstring to the related
C++/Python object.

#### 2. Building

After running the `python cli b`, the projects are built from the two "documented" directories listed above.
The output of the build will be located in the `cmake-build-release` folder. 

For Python, every binary object generated in this phase will have its own `__doc__` attribute generated
from the raw docstrings. It is possible to check this by importing the kernel (located at
`cmake-build-release/.tudatpy-documented/tudatpy/kernel.so`) into Python. From there, it is sufficient to import
a certain function or class object to check the content of its `__doc__` attribute.

In this step, the Sphinx source code is also generated and it is located in:

- `cmake-build-release/.tudat-documented/docs` for tudat
- `cmake-build-release/.tudatpy-documented/docs` for tudatpy

These are `.rst` files that will be used by Sphinx in the next step as source files. 
These source files exploit the Sphinx `autoclass` and `autofunction` commands to extract the docstring
from each Python object by accessing their `__doc__` attribute, similarly as it was explained above.


#### 3. Sphinx

After running the `python cli s`, the sphinx html files are generated. These will be located in two directories:

- `tudat-bundle/.docs-output/tudat` for tudat
- `tudat-bundle/.docs-output/tudatpy` for tudatpy

To check the output of the html files, it is recommended to open the `index.html` file with your preferred browser
(or, if you are using CLion, with CLion's built-in html viewer) and navigate through the various html pages from there.


## Common Issues

### Missing Dependencies?

Check if the `environment.yaml` file inside `tudat-bundle` contains the missing dependency (you may have the environment installed from an older file). **Not present in there?** Please post the [issue here](https://github.com/tudat-team/tudat-multidoc/issues), or add the dependency yourself.

### API Documentation not generated as expected?

Please see the section below on **Some Notes/FAQ**. If your issue is not mentioned there, **or** the templates are not as they should be yet, please post an issue on the `multidoc` [repository here](https://github.com/ggarrett13/multidoc/issues).

## Some Notes/ FAQ

**Will my build be overwritten?**

Don't worry, builds aren't discarded, only updated if changes are found in the source when executing `b/a`.

**Why are some elements not documented as expected in the output HTML?**

This is expected given our current state of development. The possibilities (I'm aware of) are:

- [**pybind**] Variants (the concept in `multidoc` used for overloads) are not dealt with yet in the generated `docstrings.h` file yet ([see here](https://github.com/ggarrett13/multidoc/blob/52bf73c593db7753b882100907541d0eb775ad2a/multidoc/templates/docstring_h.jinja2#L7)).
- [**cpp/pybind**] `multidoc` was designed with the intention of namespace-module equivalency in mind. This means that if the namespace in cpp does not match the module structure in the pybind exposure, `multidoc` cannot automagically generate the API docs. This extends to the directory structure of the `cpp` source. The following exemplar statements demonstrate this requirement:
    - `tudatpy.interface.spice` should be exposed inside a namespace in the `tudatpy` source as `tudatpy::interface::spice`.
        - Why? Because `get_docstring(element,variant)` is redefined in each namespace separately, to ensure no ambiguity when calling `get_docstring()` (e.g. `module_1.create()`/`module_2.create()`). This design was adhered to to ensure the undocumented version of `tudatpy` can be compiled with a default `get_docstring()` which returns an arbitrary `No doc found`.
    - `tudat::interface::spice` should be a namespace that encompasses all source files in a directory found as `tudat/interface/spice/*`.
        - Why? Because all API elements in `docstrings/interface/spice.yaml` are collected as a dictionary to replace all `//! get_docstring(element, variant)` tags in the tudat header files. These files are iterated through according to the defined API structure, to avoid clashes. The namespace address/location is then used to generate the sphinx `.rst` [seen here](https://github.com/ggarrett13/multidoc/blob/52bf73c593db7753b882100907541d0eb775ad2a/multidoc/templates/cpp-sphinx-module.jinja2#L55).
    - [**cpp**/**pybind**] Some elements aren't showing up? They may not be implemented correctly in the template yet. For example, module level [`Constants`](https://multidoc.readthedocs.io/en/latest/parsing.html#multidoc.parsing.Constant) are not yet implemented in the expansion of the module templates (e.g. see [py-sphinx-module.jinja2](https://github.com/ggarrett13/multidoc/blob/52bf73c593db7753b882100907541d0eb775ad2a/multidoc/templates/cpp-sphinx-module.jinja2#L37)) which use the term `Attribute` here instead incorrectly.

**Why does doxygen take so long to build?**

Unfortunately, I've yet to design a configuration of the target source directories in the `Doxyfile.in` which list only those stated in the API docstrings.
