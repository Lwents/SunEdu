# Fix Disk Space Issues on EC2

## Problem
Deploy fails with: `No space left on device`

## Quick Fix

SSH to EC2 and run:
```bash
cd /var/www/SunEdu/backend
bash fix_disk_space_now.sh
```

Then retry deployment.

## What Changed

1. **Workflow auto-cleanup** - Cleans Docker, cache before deploy
2. **Optimized Dockerfile** - Multi-stage build, smaller image
3. **Cleanup scripts** - Manual cleanup tools

## Scripts

- `fix_disk_space_now.sh` - Emergency cleanup (use now!)
- `cleanup_ec2_disk.sh` - Regular cleanup
- `setup_swap_ec2.sh` - Add swap space

## Next Steps

1. Run `fix_disk_space_now.sh` on EC2
2. Commit and push these changes
3. Retry deployment
4. Setup swap if low RAM
5. Schedule regular cleanup (cron)

## Monitor Disk

```bash
df -h /
docker system df
```

## Increase Disk (if needed)

AWS Console → EC2 → Volumes → Modify Volume → Increase size

Then on EC2:
```bash
sudo growpart /dev/xvda 1
sudo resize2fs /dev/xvda1
```
