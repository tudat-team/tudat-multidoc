# ``tudat-multidoc``

This repository contains the docstring source for the ``tudat``/``tudatpy``  
repository. This repository effectively contains a description of the Tudat 
API.

# Let's generate documented versions of `tudat`/`tudatpy` 

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

3. Generate the documented versions of `tudat` and `tudatpy`:

```bash
python make_documented.py
```

You should now have the following directories under your `tudat-bundle` 
environment. They are listed under `tudat-bundle/.gitignore`, so they will 
not be tracked.

# Let's document a new feature of `tudat`/`tudatpy` 
