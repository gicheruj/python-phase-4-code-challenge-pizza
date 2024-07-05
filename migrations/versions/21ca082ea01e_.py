"""empty message

Revision ID: 21ca082ea01e
Revises: 
Create Date: 2024-07-03 13:28:51.834469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'your_revision_id'
down_revision = 'your_previous_revision_id'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns
    op.add_column('restaurant_pizzas', sa.Column('pizza_id', sa.Integer(), nullable=False))
    op.add_column('restaurant_pizzas', sa.Column('restaurant_id', sa.Integer(), nullable=False))

    # If you need to add foreign key constraints
    op.create_foreign_key('fk_restaurant_pizzas_pizza', 'restaurant_pizzas', 'pizzas', ['pizza_id'], ['id'])
    op.create_foreign_key('fk_restaurant_pizzas_restaurant', 'restaurant_pizzas', 'restaurants', ['restaurant_id'], ['id'])


def downgrade():
    # Drop foreign key constraints if they were added
    op.drop_constraint('fk_restaurant_pizzas_pizza', 'restaurant_pizzas', type_='foreignkey')
    op.drop_constraint('fk_restaurant_pizzas_restaurant', 'restaurant_pizzas', type_='foreignkey')

    # Remove columns
    op.drop_column('restaurant_pizzas', 'pizza_id')
    op.drop_column('restaurant_pizzas', 'restaurant_id')

