"""create workspace invitations table

Revision ID: a27_wk_invites
Revises: a26_act_logs
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a27_wk_invites'
down_revision: Union[str, Sequence[str], None] = 'a26_act_logs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('workspace_invitations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workspace_id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('token_hash', sa.String(length=255), nullable=False),
    sa.Column('invited_by', sa.UUID(), nullable=True),
    sa.Column('accepted_by', sa.UUID(), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['accepted_by'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['invited_by'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token_hash')
    )
    op.create_index(op.f('ix_workspace_invitations_accepted_by'), 'workspace_invitations', ['accepted_by'], unique=False)
    op.create_index(op.f('ix_workspace_invitations_email'), 'workspace_invitations', ['email'], unique=False)
    op.create_index(op.f('ix_workspace_invitations_invited_by'), 'workspace_invitations', ['invited_by'], unique=False)
    op.create_index(op.f('ix_workspace_invitations_workspace_id'), 'workspace_invitations', ['workspace_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_workspace_invitations_workspace_id'), table_name='workspace_invitations')
    op.drop_index(op.f('ix_workspace_invitations_invited_by'), table_name='workspace_invitations')
    op.drop_index(op.f('ix_workspace_invitations_email'), table_name='workspace_invitations')
    op.drop_index(op.f('ix_workspace_invitations_accepted_by'), table_name='workspace_invitations')
    op.drop_table('workspace_invitations')
