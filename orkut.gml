graph [
  directed 1
  node [
    id 0
    label "Retrieve"
    start 0
  ]
  node [
    id 1
    label "Publish"
    start 1
  ]
  edge [
    source 0
    target 0
    weight 0.9
  ]
  edge [
    source 0
    target 1
    weight 0.1
  ]
  edge [
    source 1
    target 0
    weight 0.9
  ]
  edge [
    source 1
    target 1
    weight 0.1
  ]
]
