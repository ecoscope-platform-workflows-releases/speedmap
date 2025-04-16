# Workflow Template Repository

This repository contains a template for creating custom workflows. Follow the setup steps below to get started.

## Setup Steps

1. **Update the project name**
   
   Open the `pixi.toml` file and update the `name` field in the `[project]` section:
   ```toml
   [project]
   name = "template" #TODO: update "template" with your project name

   [tasks.pytest-cli]
   cmd = "./dev/pytest.sh template 'cli'" #TODO: update "template" with your project name

   [tasks.pytest-snapshot-update]
   cmd = "./dev/rmrf-snapshots.sh && ./dev/pytest.sh template 'app' 'sequential' --snapshot-update" #TODO: update "template" with your project name
   ```

2. **Update the workflow ID**
   
   Open the `spec.yaml` file and update the `id` field:
   ```yaml
   id: your-workflow-id
   ```

3. **Install pixi**
   
   If you don't have pixi installed, install it by following the instructions at the [official documentation](https://pixi.sh/latest/).

4. **Compile the workflow**
   
   Run the following command to compile your workflow:
   ```bash
   pixi run compile
   ```
   
   This will generate a folder called `ecoscope-workflows-<your-workflow-id>-workflow` with your compiled workflow.

5. **Generate your workflow result snapshot**
   
   Run the following command to generate your workflow result snapshot:
   ```bash
   pixi run pytest-snapshot-update
   ```

   This will generate a folder called `__results_snapshots__` with an example output.

6. **Test your workflow**
   
   Run the following command to test your workflow:
   ```bash
   pixi run pytest-cli
   ```


## Development Steps

1. **Make your changes in [ecoscope-workflow](https://github.com/wildlife-dynamics/ecoscope-workflows)**


2. **Build the ecoscope-workflow packages**
   
   ```bash
   pixi run build-release
   ```

3. **Test the changes in your workflow**
   
4. **Publish your changes**
   After merge your changes in ecoscope-workflows, bump the version by

   ```bash
   git tag v0.0.2
   git push origin --tags
   ```
   Check if the version has been successfully pushed to prefix in [Github](https://github.com/wildlife-dynamics/ecoscope-workflows/actions/workflows/publish.yml)

   Then update the version in pixi.toml
   ```toml
   [dependencies.ecoscope-workflows-core]
   channel = 'https://repo.prefix.dev/ecoscope-workflows/'
   version = '0.0.2'

   [dependencies.ecoscope-workflows-ext-ecoscope]
   channel = 'https://repo.prefix.dev/ecoscope-workflows/'
   version = '0.0.2'
   ```


## Project Structure

- `pixi.toml`: Contains project configuration including dependencies
- `spec.yaml`: Contains workflow specifications
- `test-cases.yaml`: Contains test cases for your workflow
- `layout.json`: Contains the dashboard layout settings
- `dev`: Contains scripts required for development

## Additional Resources

- [Ecoscope Core Library](https://github.com/wildlife-dynamics/ecoscope)
- [Pixi Documentation](https://pixi.sh/latest/)
