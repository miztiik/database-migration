#!/usr/bin/env python3

from aws_cdk import core

from database_migration.database_migration_stack import DatabaseMigrationStack


app = core.App()
DatabaseMigrationStack(app, "database-migration")

app.synth()
