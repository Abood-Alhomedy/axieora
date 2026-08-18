"""create chats table

Revision ID: a14_chats
Revises: a13_wf_vars
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a14_chats'
down_revision: Union[str, Sequence[str], None] = 'a13_wf_vars'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('chats',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workspace_id', sa.UUID(), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('agent_id', sa.UUID(), nullable=True),
    sa.Column('workflow_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chats_agent_id'), 'chats', ['agent_id'], unique=False)
    op.create_index(op.f('ix_chats_project_id'), 'chats', ['project_id'], unique=False)
    op.create_index(op.f('ix_chats_user_id'), 'chats', ['user_id'], unique=False)
    op.create_index(op.f('ix_chats_workflow_id'), 'chats', ['workflow_id'], unique=False)
    op.create_index(op.f('ix_chats_workspace_id'), 'chats', ['workspace_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_chats_workspace_id'), table_name='chats')
    op.drop_index(op.f('ix_chats_workflow_id'), table_name='chats')
    op.drop_index(op.f('ix_chats_user_id'), table_name='chats')
    op.drop_index(op.f('ix_chats_project_id'), table_name='chats')
    op.drop_index(op.f('ix_chats_agent_id'), table_name='chats')
    op.drop_table('chats')
