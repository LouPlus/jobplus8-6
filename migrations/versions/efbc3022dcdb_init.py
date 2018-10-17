"""init

Revision ID: efbc3022dcdb
Revises: 
Create Date: 2018-10-16 21:59:49.628820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efbc3022dcdb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=24), nullable=False),
    sa.Column('email', sa.String(length=24), nullable=False),
    sa.Column('password', sa.String(length=24), nullable=False),
    sa.Column('address', sa.String(length=36), nullable=False),
    sa.Column('logo_url', sa.String(length=24), nullable=False),
    sa.Column('company_url', sa.String(length=24), nullable=False),
    sa.Column('short_description', sa.String(length=36), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('role', sa.SmallInteger(), nullable=True),
    sa.Column('job', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('job',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jobname', sa.String(length=64), nullable=False),
    sa.Column('salary', sa.String(length=64), nullable=True),
    sa.Column('exprience', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('job_description', sa.String(length=256), nullable=True),
    sa.Column('job_requirement', sa.String(length=256), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('company')
    # ### end Alembic commands ###
