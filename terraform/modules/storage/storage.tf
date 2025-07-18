resource "google_storage_bucket" "storage-bucket" {
  name          = "tf-bucket-023258"
  location      = "us"
  force_destroy = true
  uniform_bucket_level_access = true
}
