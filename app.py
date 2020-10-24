#!/usr/bin/env python3

from aws_cdk import core
from database_migration.stacks.back_end.vpc_stack import VpcStack
from database_migration.stacks.back_end.database_migration_prerequisite_stack import DatabaseMigrationPrerequisiteStack
from database_migration.stacks.back_end.sql_client_on_ec2_stack import SqlClientOnEc2Stack
from database_migration.stacks.back_end.database_migration_stack import DatabaseMigrationStack


app = core.App()
DatabaseMigrationStack(app, "database-migration")

core.Tag.add(app, key="Owner",
             value=app.node.try_get_context("owner"))
core.Tag.add(app, key="OwnerProfile",
             value=app.node.try_get_context("github_profile"))
core.Tag.add(app, key="Project",
             value=app.node.try_get_context("service_name"))
core.Tag.add(app, key="GithubRepo",
             value=app.node.try_get_context("github_repo_url"))
core.Tag.add(app, key="Udemy",
             value=app.node.try_get_context("udemy_profile"))
core.Tag.add(app, key="SkillShare",
             value=app.node.try_get_context("skill_profile"))
core.Tag.add(app, key="AboutMe",
             value=app.node.try_get_context("about_me"))
core.Tag.add(app, key="BuyMeACoffee",
             value=app.node.try_get_context("ko_fi"))


app.synth()
