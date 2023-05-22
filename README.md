# Recipe Wizard

This app is the starting point for all of our 
Vue applications.  To write a new Vue app 
in py4web, clone this application in your apps 
folder, and work on it. 

## Clone this repo into your local Py4Web Apps folder
```
cd /py4web
git clone https://github.com/CarsonWebster/RecipeWizard.git ./apps/RecipeWizard
```
Or if currently in apps folder
```
git clone https://github.com/CarsonWebster/RecipeWizard.git
```

## Pull request model
When developing a new feature yourself, with a pair, or together as a team, create a feature branch to avoid merge conflicts. Remeber to pull frequently before starting a coding session. 
Creating a new branch:
```
git branch <branch_name>
```
Listing branches:
```
git branch
```
Checkout a local branch
```
git checkout <branch_name>
```
Checkout a remote branch (origin / from github)
```
git checkout -b <branch_name> origin/<branch_name>
```
Your feature branch should contain your contributions for a given feature.

When developing, comming your changes as you go, with short relevalnt commit messages
```
git add <files>
git commit -m "Git commit message"
```

And push to the origin/github repository to make the branch visible. -u also sets this branch to be the default upstream branch for future pushes
```
git push -u origin <branch_name>
```

When a feature on a branch is implemented and pushed, create a pull request on the github repo with a relevant longer description of the feature and changes. This starts the review process, allowing others to review and accept/deny the changes. If one other person submits a review message, those changes can be merged into the main branch.

This models allows multiple contributors to work simultaneously, reducing the risk of nasty merge conflicts. 

Remember to set your git name and email
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

And pull rebase option set to true. Pull frequently! :)
```
git config --global pull.rebase true
```
