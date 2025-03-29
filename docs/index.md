---
hide:
  - navigation
  - toc
---

# SLC-CC Tech Team Documentation Site

About SLC Tech Team: [SLC-CC Tech Team Page](https://clubs.iiit.ac.in/tech-team)

GitHub Organisation: [Clubs-Council-IIITH](https://github.com/Clubs-Council-IIITH)

## Current Maintainers

- [Bhav Beri](https://github.com/bhavberi)
- [Adari Dileepkumar](https://github.com/Dileepadari)
- [Abhiram Tilak](https://github.com/abhiramtilakiiit)
- [Shreyansh](https://github.com/The-Broken-Keyboard)
- [Evan Bijoy](https://github.com/EvanBijoy)

Contact Us: [webadmin@students.iiit.ac.in](mailto:webadmin@students.iiit.ac.in) or [clubs@iiit.ac.in](mailto:clubs@iiit.ac.in)

## Deployment Status

> [![Better Uptime Badge](https://betteruptime.com/status-badges/v3/monitor/ikqm.svg)](https://clubs_iiith.betteruptime.com/)

[https://clubs.iiit.ac.in](https://clubs.iiit.ac.in/) & [https://life.iiit.ac.in](https://life.iiit.ac.in/) both point to the same website. Currently, [https://life.iiit.ac.in](https://life.iiit.ac.in/) is only within the IIIT-H network.

Website `v2` released in April, 2023.

## Architecture

![Architecture](https://raw.githubusercontent.com/Clubs-Council-IIITH/.github/main/profile/cc-arch.png)

## Repository Structure

![Maintenance](https://img.shields.io/maintenance/yes/2026)

- [Web Client (Frontend)](https://github.com/Clubs-Council-IIITH/web)

  ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/web)
  [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/web)](https://libraries.io/github/Clubs-Council-IIITH/web)

  ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/web?style=plastic)

- [MicroServices (Backend) + Nginx](https://github.com/Clubs-Council-IIITH/services)

  ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/services)
  [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/services)](https://libraries.io/github/Clubs-Council-IIITH/services)

  ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/services?style=plastic)

  - [Authentication Service](https://github.com/Clubs-Council-IIITH/auth)

  - [Development Authentication Service](https://github.com/Clubs-Council-IIITH/auth-dev)

  - [Files Service](https://github.com/Clubs-Council-IIITH/files)

  - [Clubs Service](https://github.com/Clubs-Council-IIITH/clubs)

    ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/clubs)
    [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/clubs)](https://libraries.io/github/Clubs-Council-IIITH/clubs)

    ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/clubs?style=plastic)

  - [Members Service](https://github.com/Clubs-Council-IIITH/members)

    ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/members)
    [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/members)](https://libraries.io/github/Clubs-Council-IIITH/members)

    ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/members?style=plastic)

  - [Events Service](https://github.com/Clubs-Council-IIITH/events)

    ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/events)
    [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/events)](https://libraries.io/github/Clubs-Council-IIITH/events)

    ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/events?style=plastic)

  - [Users Service](https://github.com/Clubs-Council-IIITH/users)

    ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/users)
    [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/users)](https://libraries.io/github/Clubs-Council-IIITH/users)

    ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/users?style=plastic)

  - [Interfaces Service](https://github.com/Clubs-Council-IIITH/interfaces)

    ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/interfaces)
    [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/interfaces)](https://libraries.io/github/Clubs-Council-IIITH/interfaces)

    ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/interfaces?style=plastic)

- [Gateway Service (Microservices)](https://github.com/Clubs-Council-IIITH/gateway)

  ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/gateway)
  [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/gateway)](https://libraries.io/github/Clubs-Council-IIITH/gateway)

  ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/gateway?style=plastic)

  - [<span style="text-decoration: line-through;">Composer Service</span>](https://github.com/Clubs-Council-IIITH/composer) _(Deprecated & merged into gateway service itself & in microservices)_

      <!-- ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/composer)
      <> [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/composer)](https://libraries.io/github/Clubs-Council-IIITH/composer) -->

      <!-- ![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/composer?style=plastic) -->

- [<span style="text-decoration: line-through;">Feeder Service Config</span>](https://github.com/Clubs-Council-IIITH/feeder) _(Deprecated)_

    <!--![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/feeder) -->
    <!-- [![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/Clubs-Council-IIITH/feeder)](https://libraries.io/github/Clubs-Council-IIITH/feeder) -->

    <!--![GitHub language count](https://img.shields.io/github/languages/count/Clubs-Council-IIITH/feeder?style=plastic) -->

- [Reverse Proxy Server Config](https://github.com/Clubs-Council-IIITH/reverse-proxy)

  ![GitHub last commit](https://img.shields.io/github/last-commit/Clubs-Council-IIITH/reverse-proxy)

---

### Build Details

Built Commit: Version 2.2 - [#{{ git_commit}}](https://github.com/Clubs-Council-IIITH/services/commit/{{ git_commit}})<br/>
Last Updated: {{ build_date }}<br/>
Currently deployed version: [#{{ git.short_commit}}](https://github.com/Clubs-Council-IIITH/api-docs/commit/{{ git.short_commit}})

Built with [MkDocs](https://www.mkdocs.org).