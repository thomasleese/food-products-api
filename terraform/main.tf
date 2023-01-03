terraform {
  required_version = "1.3.6"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    sentry = {
      source  = "jianyuan/sentry"
      version = "~> 0.11"
    }
  }

  cloud {
    organization = "thomasleese"

    workspaces {
      name = "food-products-api"
    }
  }
}

provider "digitalocean" {
  token = var.digitalocean_token
}

provider "sentry" {
  token = var.sentry_token
}

resource "sentry_project" "main" {
  organization = var.sentry_organization
  teams        = [var.sentry_team]
  slug         = "food-products-api"
  name         = "Food Products API"
  platform     = "python-fastapi"
}

resource "sentry_key" "main" {
  organization = sentry_project.main.organization
  project      = sentry_project.main.slug
  name         = "Default"
}

resource "digitalocean_app" "main" {
  spec {
    name   = "food-products-api"
    region = "lon"

    alert {
      rule = "DEPLOYMENT_FAILED"
    }

    alert {
      rule = "DOMAIN_FAILED"
    }

    env {
      key   = "SENTRY_DSN"
      type  = "SECRET"
      value = sentry_key.main.dsn_public
    }

    service {
      name = "web"

      run_command      = "gunicorn -k uvicorn.workers.UvicornWorker --pythonpath src food_products_api.web:app"
      environment_slug = "python"

      instance_size_slug = "basic-xxs"
      instance_count     = 1

      http_port = 8000

      github {
        repo           = "thomasleese/food-products-api"
        branch         = "main"
        deploy_on_push = true
      }

      routes {
        path = "/"
      }
    }
  }
}

resource "digitalocean_project" "main" {
  name        = "Food Products API"
  environment = "Production"
}

resource "digitalocean_project_resources" "main" {
  project = digitalocean_project.main.id
  resources = [
    digitalocean_app.main.urn
  ]
}
