from mage_ai.data_cleaner.transformer_actions.constants import ImputationStrategy
from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pyspark.sql import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.IMPUTE

    Docs: https://docs.mage.ai/guides/transformer-blocks#fill-in-missing-values
    """

    columns_to_impute = ['low', 'high', 'open', 'close', 'volume']
    
    action = build_transformer_action(
        df,
        action_type=ActionType.IMPUTE,
        arguments=columns_to_impute,  # Specify column to impute
        axis=Axis.COLUMN,
        options={'strategy': ImputationStrategy.MEDIAN},  # Specify imputation strategy
    )

    df = BaseAction(action).execute(df)

    df = df.dropna(subset=['token', 'date'])

    return BaseAction(action).execute(df)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
