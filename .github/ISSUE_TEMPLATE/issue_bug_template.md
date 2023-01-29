name: Bug
description: Bug report
body:
  - type: input
    id: distro
    attributes:
      label: Linux distribution
      description: "Write the name and version of the distribution"
      placeholder: "e.g. Fedora 37, Ubuntu 22.04"
    validations:
      required: true  
  - type: input
    id: desktop
    attributes:
      label: Desktop environment
      description: "Write the name and version of Desktop environment"
      placeholder: "e.g. GNOME 43, KDE Plasma 5.24"
    validations:
      required: true
  - type: input
    id: timerver
    attributes:
      label: Version of Timer
      description: "Write the version of Timer. If a new version of Timer is not available after checking for updates in a software management program (e.g. GNOME Software, KDE Discover), type 'latest' in the text box below"
      placeholder: "e.g. latest"
    validations:
      required: true
  - type: textarea
    id: stepstoreproduce
    attributes:
      label: Bug description
      description: What happened?
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Which steps do we need to take to reproduce this error?
