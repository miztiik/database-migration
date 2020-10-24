from aws_cdk import aws_cloudformation as cfn
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import core


class SshKeyGeneratorStack(core.Construct):
    def __init__(
            self,
            scope: core.Construct,
            id: str,
            ssh_key_name="mystique-automation-ssh-key",
            ** kwargs
    ) -> None:
        super().__init__(scope, id)

        # Read Lambda Code:)
        try:
            with open("custom_resources/ssh_key_generator/lambda_src/index.py",
                      encoding="utf-8",
                      mode="r"
                      ) as f:
                ssh_key_generator_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")
            raise

        # Create IAM Permission Statements that are required by the Lambda

        role_stmt1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ec2:CreateKeyPair",
                "ec2:DeleteKeyPair"
            ]
        )
        role_stmt1.sid = "AllowLambdaToCreateSshKey"
        role_stmt2 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ssm:PutParameter",
                "ssm:DeleteParameter",
                "ssm:GetParameter"
            ]
        )
        role_stmt2.sid = "AllowLambdaToCreateSSMParameter"

        ssh_key_generator_fn = _lambda.SingletonFunction(
            self,
            "sshKeyGeneratorSingleton",
            uuid="mystique30-4ee1-11e8-9c2d-fa7ae01bbebc",
            code=_lambda.InlineCode(
                ssh_key_generator_fn_code),
            handler="index.lambda_handler",
            timeout=core.Duration.seconds(10),
            runtime=_lambda.Runtime.PYTHON_3_7,
            reserved_concurrent_executions=1,
            environment={
                "LOG_LEVEL": "INFO",
                "APP_ENV": "Production",
                "SSH_KEY_NAME": ssh_key_name
            },
            description="Creates a SSH Key in the region"
        )

        ssh_key_generator_fn.add_to_role_policy(role_stmt1)
        ssh_key_generator_fn.add_to_role_policy(role_stmt2)

        # Create Custom Log group
        ssh_key_generator_fn_lg = _logs.LogGroup(
            self,
            "sshKeyGeneratorLogGroup",
            log_group_name=f"/aws/lambda/{ssh_key_generator_fn.function_name}",
            retention=_logs.RetentionDays.ONE_WEEK,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        ssh_key_generator = cfn.CustomResource(
            self,
            "sshKeyGeneratorCustomResource",
            provider=cfn.CustomResourceProvider.lambda_(
                ssh_key_generator_fn
            ),
            properties=kwargs,
        )

        self.response = ssh_key_generator.get_att(
            "ssh_key_gen_status").to_string()
