variable "name" {
  type        = string
  default     = "default"
  description = " (Required) A unique name for the resource, required by GCE. Changing this forces a new resource to be created"
}

variable "machine_type" {
  type        = string
  default     = "n1-standard-4"
  description = "(Required) The machine type to create"
}

variable "services" {
  type = list(string)
  default = [
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com"
  ]
}

variable "zone" {
  type        = string
  default     = "europe-north1-c"
  description = "(Optional) The zone that the machine should be created in. If it is not provided, the provider zone is used."
}

variable "image" {
  type        = string
  #default     = "cos-cloud/cos-stable-97-16919-29-34" 
  default     = "ubuntu-os-cloud/ubuntu-2004-lts"
  description = "The image from which to initialize this disk. This can be one of: the image's self_link, projects/{project}/global/images/{image}, projects/{project}/global/images/family/{family}, global/images/{image}, global/images/family/{family}, family/{family}, {project}/{family}, {project}/{image}, {family}, or {image}. If referred by family, the images names must include the family name. If they don't, use the google_compute_image data source. For instance, the image centos-6-v20180104 includes its family name centos-6. These images can be referred by family name here."
}

variable "region" {
  type        = string
  default     = "europe-north1"
  description = "Name of Region."
}

variable "description" {
  type        = string
  default     = ""
  description = "(optional) A brief description of this resource."
}

variable "gce_ssh_user" {
  type        = string
  default     = "terraform"
  description = "Do NOT change, responsible for running script."
}

