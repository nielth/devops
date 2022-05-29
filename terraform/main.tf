provider "google" {
  credentials = "${file("access.json")}"
  project = var.project
  region  = var.region
}

resource "google_compute_instance" "default" {
  name         = var.name
  machine_type = var.machine_type
  zone         = var.zone
  tags         = ["docker-node"]
  description  = var.description
  allow_stopping_for_update = "true"

  boot_disk {
    initialize_params {
      image = var.image
      size = 50
    }
  }
  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-keys = "${var.gce_ssh_user}:${file("./ssh/id_rsa.pub")}"
  }

  connection {
    type = "ssh"
    user = "${var.gce_ssh_user}"
    private_key = "${file("./ssh/id_rsa")}"
    agent = "false"
    host = self.network_interface[0].access_config[0].nat_ip
  }

  provisioner "file" {
    source = "../src"
    destination = "."
  }

  provisioner "remote-exec" {
    script = "./docker.sh"
  }
}

resource "google_compute_firewall" "default" {
  name    = "custom-firewall-internal"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "2224", "81"]
  }

  target_tags   = ["docker-node"]
  source_ranges = [var.public_ip]
}



