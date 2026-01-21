"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("create extension if not exists pgcrypto")

    op.execute(
        """
        create table if not exists users (
          id uuid primary key default gen_random_uuid(),
          email text not null unique,
          password_hash text not null,
          role text not null check (role in ('ADMIN','USER')),
          is_active boolean not null default true,
          created_at timestamptz not null default now()
        );
        """
    )

    op.execute(
        """
        create table if not exists partners (
          id uuid primary key default gen_random_uuid(),
          name text not null,
          code text not null unique,
          workflow_key text not null,
          default_currency text not null default 'PLN',
          is_active boolean not null default true,
          created_at timestamptz not null default now()
        );
        """
    )

    op.execute(
        """
        create table if not exists partner_routing_rules (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id) on delete cascade,
          rule_name text not null,
          rule_json jsonb not null default '{}'::jsonb,
          target_json jsonb not null default '{}'::jsonb,
          is_active boolean not null default true,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_partner_routing_rules_partner
          on partner_routing_rules(partner_id);
        """
    )

    op.execute(
        """
        create table if not exists import_batches (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id),
          source_filename text not null,
          source_file_hash text not null,
          uploaded_by_user_id uuid references users(id),
          status text not null check (status in ('uploaded','parsing','parsed','failed')),
          rows_total int not null default 0,
          rows_success int not null default 0,
          rows_failed int not null default 0,
          errors_json jsonb,
          uploaded_at timestamptz not null default now(),
          parsed_at timestamptz
        );
        create unique index if not exists uq_import_batches_partner_hash
          on import_batches(partner_id, source_file_hash);
        """
    )

    op.execute(
        """
        create table if not exists import_rows (
          id uuid primary key default gen_random_uuid(),
          import_batch_id uuid not null references import_batches(id) on delete cascade,
          row_number int not null,
          raw_row jsonb not null,
          normalized_row jsonb,
          status text not null check (status in ('ok','failed','skipped')),
          error_message text,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_import_rows_batch
          on import_rows(import_batch_id);
        """
    )

    op.execute(
        """
        create table if not exists calc_programs (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id),
          code text not null,
          name text,
          valid_from date,
          valid_to date,
          currency text not null default 'PLN',
          created_at timestamptz not null default now(),
          unique (partner_id, code)
        );
        create index if not exists idx_calc_programs_partner
          on calc_programs(partner_id);
        """
    )

    op.execute(
        """
        create table if not exists calc_vehicles (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id),
          make text not null,
          model text not null,
          trim text,
          full_name text,
          external_model_key text,
          meta jsonb not null default '{}'::jsonb,
          created_at timestamptz not null default now(),
          unique (partner_id, make, model, trim, external_model_key)
        );
        create index if not exists idx_calc_vehicles_partner_make_model
          on calc_vehicles(partner_id, make, model);
        """
    )

    op.execute(
        """
        create table if not exists calc_lines (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id),
          calc_program_id uuid not null references calc_programs(id) on delete cascade,
          import_batch_id uuid not null references import_batches(id) on delete restrict,
          calc_vehicle_id uuid not null references calc_vehicles(id) on delete restrict,
          term_months int not null,
          annual_mileage_km int not null,
          total_mileage_km int not null,
          list_price_gross numeric,
          discounted_price_gross numeric,
          discount_pct numeric,
          registration_fee_gross numeric,
          rv_table text,
          rv_id text,
          rv_base_pct numeric,
          rv_adj_pct numeric,
          rv_pct numeric,
          rv_amount numeric,
          rm_table text,
          rm_id text,
          rm_val numeric,
          rm_val_per_km numeric,
          rm_amount numeric,
          amortization_amount numeric,
          book_value_y1 numeric,
          book_value_y2 numeric,
          book_value_y3 numeric,
          book_value_y4 numeric,
          raw_row jsonb not null default '{}'::jsonb,
          created_at timestamptz not null default now(),
          unique (calc_program_id, calc_vehicle_id, term_months, total_mileage_km)
        );
        create index if not exists idx_calc_lines_vehicle
          on calc_lines(calc_vehicle_id);
        create index if not exists idx_calc_lines_partner_program
          on calc_lines(partner_id, calc_program_id);
        """
    )

    op.execute(
        """
        create table if not exists calc_cost_components (
          id uuid primary key default gen_random_uuid(),
          calc_line_id uuid not null references calc_lines(id) on delete cascade,
          component_code text not null,
          label text not null,
          amount numeric,
          unit text not null check (unit in ('MONTHLY','UPFRONT','PER_KM','PER_TYRE','PER_SET','OTHER')),
          meta jsonb not null default '{}'::jsonb,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_calc_cost_components_line
          on calc_cost_components(calc_line_id);
        """
    )

    op.execute(
        """
        create table if not exists vehicles_catalog (
          id uuid primary key default gen_random_uuid(),
          title text not null,
          make text not null,
          model text not null,
          trim text,
          year int,
          description text,
          spec_json jsonb not null default '{}'::jsonb,
          is_published boolean not null default false,
          created_by_user_id uuid references users(id),
          created_at timestamptz not null default now(),
          updated_at timestamptz
        );
        create index if not exists idx_vehicles_catalog_published
          on vehicles_catalog(is_published);
        """
    )

    op.execute(
        """
        create table if not exists vehicle_images (
          id uuid primary key default gen_random_uuid(),
          vehicle_catalog_id uuid not null references vehicles_catalog(id) on delete cascade,
          storage_key text not null,
          public_url text not null,
          sort_order int not null default 0,
          alt text,
          is_cover boolean not null default false,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_vehicle_images_vehicle
          on vehicle_images(vehicle_catalog_id);
        """
    )

    op.execute(
        """
        create table if not exists vehicle_links (
          id uuid primary key default gen_random_uuid(),
          vehicle_catalog_id uuid not null references vehicles_catalog(id) on delete cascade,
          calc_vehicle_id uuid not null references calc_vehicles(id) on delete restrict,
          match_confidence numeric,
          created_at timestamptz not null default now(),
          unique (vehicle_catalog_id, calc_vehicle_id)
        );
        create index if not exists idx_vehicle_links_calc_vehicle
          on vehicle_links(calc_vehicle_id);
        """
    )

    op.execute(
        """
        create table if not exists offers (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id),
          import_batch_id uuid not null references import_batches(id) on delete restrict,
          calc_line_id uuid references calc_lines(id) on delete set null,
          calc_vehicle_id uuid references calc_vehicles(id) on delete set null,
          external_offer_id text,
          term_months int not null,
          annual_mileage_km int not null,
          total_mileage_km int,
          currency text not null default 'PLN',
          vat_rate numeric,
          upfront_fee_net numeric,
          upfront_fee_gross numeric,
          monthly_total_net numeric,
          monthly_total_gross numeric,
          valid_from date,
          valid_to date,
          notes text,
          raw_row jsonb not null default '{}'::jsonb,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_offers_partner_term_mileage
          on offers(partner_id, term_months, annual_mileage_km);
        create index if not exists idx_offers_calc_vehicle
          on offers(calc_vehicle_id);
        create index if not exists idx_offers_monthly_total_net
          on offers(monthly_total_net);
        """
    )

    op.execute(
        """
        create table if not exists offer_components (
          id uuid primary key default gen_random_uuid(),
          offer_id uuid not null references offers(id) on delete cascade,
          component_code text not null,
          label text not null,
          amount_net numeric,
          amount_gross numeric,
          unit text not null check (unit in ('MONTHLY','UPFRONT','PER_KM_OVER','PER_KM_UNDER','OTHER')),
          included boolean not null default true,
          meta jsonb not null default '{}'::jsonb,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_offer_components_offer
          on offer_components(offer_id);
        """
    )

    op.execute(
        """
        create table if not exists leads (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id),
          offer_id uuid not null references offers(id) on delete restrict,
          status text not null check (status in ('new','contacted','qualified','won','lost')),
          contact_json jsonb not null,
          notes text,
          source text,
          assigned_to_user_id uuid references users(id),
          created_at timestamptz not null default now(),
          routed_at timestamptz,
          routing_result_json jsonb
        );
        create index if not exists idx_leads_partner_status
          on leads(partner_id, status);
        create index if not exists idx_leads_assigned_to
          on leads(assigned_to_user_id);
        """
    )

    op.execute(
        """
        create table if not exists lead_events (
          id uuid primary key default gen_random_uuid(),
          lead_id uuid not null references leads(id) on delete cascade,
          event_type text not null,
          payload jsonb not null default '{}'::jsonb,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_lead_events_lead
          on lead_events(lead_id);
        """
    )

    op.execute(
        """
        create table if not exists partner_import_templates (
          id uuid primary key default gen_random_uuid(),
          partner_id uuid not null references partners(id) on delete cascade,
          template_type text not null check (template_type in ('OFFERS','CALC_RATECARD')),
          name text not null,
          config_json jsonb not null,
          is_active boolean not null default true,
          created_at timestamptz not null default now()
        );
        create index if not exists idx_partner_import_templates_partner
          on partner_import_templates(partner_id, template_type, is_active);
        """
    )


def downgrade() -> None:
    op.execute("drop table if exists partner_import_templates")
    op.execute("drop table if exists lead_events")
    op.execute("drop table if exists leads")
    op.execute("drop table if exists offer_components")
    op.execute("drop table if exists offers")
    op.execute("drop table if exists vehicle_links")
    op.execute("drop table if exists vehicle_images")
    op.execute("drop table if exists vehicles_catalog")
    op.execute("drop table if exists calc_cost_components")
    op.execute("drop table if exists calc_lines")
    op.execute("drop table if exists calc_vehicles")
    op.execute("drop table if exists calc_programs")
    op.execute("drop table if exists import_rows")
    op.execute("drop table if exists import_batches")
    op.execute("drop table if exists partner_routing_rules")
    op.execute("drop table if exists partners")
    op.execute("drop table if exists users")
    op.execute("drop extension if exists pgcrypto")
