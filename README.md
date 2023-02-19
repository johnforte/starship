## Starship

Want to manage a small cluster of ec2's with ease.

## What this does not do...
1) It will not load balance containers across ec2's, it will run a composer file per ec2, which should have replicas defined for that.
2) It will not spin up load balancer, instead it will us route 53 as a DNS load balancer, by registering the current ip.


## What does this actually do...
1) Listen for registry updates.
