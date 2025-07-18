# Terraform Directory

This directory contains the Terraform configuration files used to provision and manage resources on Google Cloud Platform (GCP).

## Structure

The structure of the `terraform` directory is organized as follows:

- **main.tf**: The main entry point for Terraform configuration. Contains resource definitions and module calls.
- **variables.tf**: Defines the variables used in the Terraform configurations.
- **outputs.tf**: Specifies the outputs that will be displayed after applying the Terraform plan.
- **terraform.tfvars**: Contains the values for the variables defined in `variables.tf`. You can use this file to customize your deployment.
- **modules/**: (optional) Contains reusable modules that can be referenced in `main.tf`.


> **Note:** Some files or folders might not be present if your setup does not require them.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed (version 1.0 or higher recommended)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and initialized
- Access to a GCP account with sufficient permissions

## Basic Commands

Below are the main commands to manage your infrastructure using Terraform:

### 1. Initialize the Terraform Working Directory

```sh
terraform init
```

This command downloads the necessary provider plugins and prepares the backend.

### 2. Review the Execution Plan

```sh
terraform plan
```

This command shows what changes will be made to your infrastructure.

### 3. Apply the Terraform Configuration

```sh
terraform apply
```

This command provisions the resources defined in your configuration files. You will be prompted to approve the changes.

### 4. Destroy the Infrastructure

```sh
terraform destroy
```

This command deletes all resources managed by this Terraform configuration.

## Usage Example

```sh
# Move into the terraform directory
cd terraform

# Initialize Terraform
terraform init

# (Optional) Format the code
terraform fmt

# Validate configuration
terraform validate

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply
```

## Environment Variables

You may need to set some environment variables for authentication or configuration, such as:

```sh
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```
