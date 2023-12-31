## REQUIREMENTS

[Requirements Page](https://bitespeed.notion.site/Bitespeed-Backend-Task-Identity-Reconciliation-53392ab01fe149fab989422300423199)

## NOTES

* The app is currently deployed at [https://bitespeed.arm.ravimakes.com/](https://bitespeed.arm.ravimakes.com/)
  * There are two endpoints:
    * /identify - The required endpoint to identify user
    * /reset - Removes all users
* Github repo at [bitespeed-interview](https://github.com/ravikiranp123/bitespeed-interview)
* This app is built using Django for now. I chose Django to avoid building/setting up scaffolding such as ORM. Django makes it easy with built in ORMs, migrations and a dashboard.
* I will rebuild this using express and typescript when I get some time
* The logic of identity reconciliation is in bitespeed/identity_reconciliation/recon_logic.py
  * At a high level, there are multiple 'rules' defined. Such as a rule when no matches are found => create a new primary user
  * These rules are looped through and stopped when a rule succeeds.
  * A helper function then fetches all users where either their id or their linkedId matches the id/linkedId of the returned user
* This project has CI/CD built in
* I am currently using Docker and Caprover to deploy on an Oracle virtual machine

## TODO

* [ ] Write tests
* [ ] Improve documentation
* [ ] Rewrite with express and typescript
