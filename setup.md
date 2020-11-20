# Setup

-----

```sh
git clone https://github.com/csc301-fall-2020/team-project-13-lady-ballers-camp-backend.git
cd ./team-project-13-lady-ballers-camp-backend
```

## 1. Setup python environment:

Run `conda env create -f environment.yml` to create an environment called "fast-api",  as defined in `environment.yml`.

After running `conda env create -f environment.yml` activate the new environment and install the requirements:

```sh
conda activate fast-api
pip-sync requirements.txt requirements-dev.txt
```

If you add, remove, or need to update versions of some requirements, edit the `.in` files, then run the following:

```sh
pip-compile requirements.in && pip-compile requirements-dev.in
```

## 2. Install pre-commit hooks

Once you are in the root directory and activated the dev-environment don't forget to run `pre-commit install` each time you clone the repo.

### Notes:

- Make sure you [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

- Each time you work in this directory make sure to run `conda activate fast-api` to activate the conda environment.

  

  

