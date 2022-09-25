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

## How to trigger a build of the online API docs

- They reside at https://tudatpy.readthedocs.io/en/latest/
- They are re-built when changes are pushed to tudatpy/develop
- They use the tudat-multidoc/docstrings specified by this [git hash](https://github.com/tudat-team/tudatpy/blob/354c6492246c84822eb8d96c8c89b1a026cf674f/docs/source/conf.py#L32)

Currently there’s no version kept track of, we can sort that out later down the line. The workflow is:
1. Push your changes to tudat-multidoc
2. Change the tudat-multidoc git hash in tudatpy/develop [here](https://github.com/tudat-team/tudatpy/blob/354c6492246c84822eb8d96c8c89b1a026cf674f/docs/source/conf.py#L32)
3. Push the changes, build can be monitored [here](https://readthedocs.org/projects/tudatpy/builds/)

Note: Builds take 21.5 minutes to complete, as the tudatpy source needs to be compiled.

## Common Issues

### Missing Dependencies?

Check if the `environment.yaml` file inside `tudat-bundle` contains the missing dependency (you may have the environment installed from an older file). **Not present in there?** Please post the [issue here](https://github.com/tudat-team/tudat-multidoc/issues), or add the dependency yourself.

### API Documentation not generated as expected?

Please see the section below on **Some Notes/FAQ**. If your issue is not mentioned there, **or** the templates are not as they should be yet, please post an issue on the `multidoc` [repository here](https://github.com/ggarrett13/multidoc/issues).


## Troubleshooting Docstrings
As a developer contributing to the `yaml` source files in `tudat-multidoc/docstrings`, you are likely to encounter issues during execution of `CLI document`.
Typically, the issues are one of the following two kinds:

### Syntax issues during parsing of "filtered" yaml files
In the filtering process, the parser separates the cpp and python specific information of the `yaml` source. 
It does so by parsing only `# [cpp]` and `# [py]` tagged lines, respectively, along with the agnostic (untagged) lines of the source.
This means that the `yaml` source has to match the syntax expected by the parser, when only considering these subsets of lines. 
It is difficult to keep track of the syntax of the filtered `yaml`, therefore errors like the following will arise frequently:

```bash
5897-INFO-Parsing yaml file: ./tudat-multidoc/docstrings/numerical_simulation/environment_setup/ephemeris.yaml with kwargs: {'py': True}
5897-ERROR-Broken .yaml file ./tudat-multidoc/docstrings/numerical_simulation/environment_setup/ephemeris.yaml dumped as BROKEN-{'py': True}-ephemeris.yaml.

[...]

  in "<unicode string>", line 46, column 9:
            extended_summary: "Instances of  ... 
            ^
expected <block end>, but found '<scalar>'
  in "<unicode string>", line 58, column 21:
        short_summary: "Class for defining settings from ... 
                        ^
```
#### Interpreting error message
The first line
```bash
5897-INFO-Parsing yaml file: ./tudat-multidoc/docstrings/numerical_simulation/environment_setup/ephemeris.yaml with kwargs: {'py': True}
```
indicates the `yaml` source file (`ephemeris.yaml`) and filtering settings (`kwargs: {'py': True}`) during which the error occured.
The second line is key to troubleshooting this issue:

```bash
5897-ERROR-Broken .yaml file ./tudat-multidoc/docstrings/numerical_simulation/environment_setup/ephemeris.yaml dumped as BROKEN-{'py': True}-ephemeris.yaml.
```

It states that an auxiliary file `BROKEN-{'py': True}-ephemeris.yaml` has been dumped in `./` (i.e. on the same level as `tudat-multidoc`). 
This file shows what the parser "sees" under the current filtering settings (`kwargs: {'py': True}`). 
The syntax issue can be found in the line that is indicated by the traceback in 

```bash
yaml.parser.ParserError: while parsing a block mapping
  in "<unicode string>", line 46, column 9:
            extended_summary: "Instances of  ... 
            ^
```
where the line count does not refer to the `yaml` source, but only includes the lines that pass the filter, therefore matching the 
line count of the auxiliary file.
Following this trace in the auxiliary file, the syntax issue should become apparent. 
Note that in many cases, the second error is due to the same issue as the first error and will be disappear after resolution of the first one. 

#### Resolving the issue
In most cases the underlying issue that a missing or erroneous `# [py]` / `# [cpp]` tag. 
Consequently, the affected line or block of text passes the filter, mistakenly appearing in the filtered `yaml`.
The erroneous line or block then often does not relate well to the rest of the `yaml`, raising a parser error of some kind.

> **IMPORTANT**: Since the auxiliary file is used to inspect the error, one may accidentally perform the corrections on 
> the auxiliary file, leaving the source unchanged and not resolving the issue. In order to avoid frustration, ensure 
> to implement in the corresponding section(s) of the *source* file.


### Pydantic issues

In `tudat-multidoc/multidoc/multidoc/parsing/models.py` the pydantic python module is used in order to define data models 
for formatting the information that is eventually assembled in the API reference. Every key in the `yaml` source, such as `classes`
`functions`, `methods`, `properties`, etc refers to such a data model and/or an attribute thereof.
In order to be formatted correctly, the information grouped under each key has to be compatible with the data model 
the key refers to, else pydantic raises `validation errors`. 
An example of such an error is given below:

```bash

58600-INFO-Parsing yaml file: ./tudat-multidoc/docstrings/simulation/environment_setup/ephemeris.yaml with kwargs: {'py': True}

[...]

File "pydantic/main.py", line 406, in pydantic.main.BaseModel.__init__
pydantic.error_wrappers.ValidationError: 2 validation errors for Module
classes -> 0 -> methods -> 1 -> returns -> description
  field required (type=value_error.missing)
functions -> 2 -> returns -> type
  field required (type=value_error.missing)

```
#### Interpreting error message
The first line 
```bash
58600-INFO-Parsing yaml file: ./tudat-multidoc/docstrings/simulation/environment_setup/ephemeris.yaml with kwargs: {'py': True}
```
indicates the file in which the pydantic issue occurred, i.e. ```ephemeris.yaml```.
The next lines
```bash
File "pydantic/main.py", line 406, in pydantic.main.BaseModel.__init__
pydantic.error_wrappers.ValidationError: 2 validation errors for Module
```
state the kind of error (```validation error```) as well as the amount of errors encountered.
Next, the problematic instances of data classes are stated
```bash
classes -> 0 -> methods -> 1 -> returns -> description
  field required (type=value_error.missing)
```
This reads as "in first instance (index 0) of a `class` data model, second (index 1) instance of a `method` data model,
the `return` entry is missing a data field (named `description`), which is required by the `return` data model."
The count of instances at the highest level (i.e. in this case `classes -> 0`) refers to the counts of `class`
data structures within the aforementioned file ```ephemeris.yaml```.
Analogously the other validation error 

```bash
functions -> 2 -> returns -> type
  field required (type=value_error.missing)
```

can be read as "in third instance (index 2) of a `function` data model, the `return` entry is missing a data field 
(named `type`), which is required by the `return` data model."


> **NOTE**: In a continuous effort to make the pydantic data models more lenient, the data fields `description` and `type` 
> have been declared to be *optional* fields in the `return` data model. Therefore, the specific errors above may not
> arise in this exact form anymore, but serve a demonstrative purpose.

#### Resolving the issue
Pydantic validation errors can easily be resolved by providing the missing data field to the data structure in the `yaml` source.
In selected cases it may be a better solution to change the troubling pydantic data model to be more lenient, i.e. making the missing data field 
an *optional* member of the data model.



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
