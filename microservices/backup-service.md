# Backup Service

## Responsibility
Backend/infrastructure-level database backup and restore orchestration.

## Rules
- PWA never performs backups;
- backups are encrypted;
- restore requires the recovery/encryption key according to the documented procedure;
- key is exposed only at initial creation/initialization as specified;
- database persistence survives container replacement;
- restore procedures must be tested on the NAS.

This service may be implemented as infrastructure tooling rather than a permanently running container if that is safer/lighter.