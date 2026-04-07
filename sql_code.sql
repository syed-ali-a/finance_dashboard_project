CREATE TABLE chart_of_accounts (
    id SERIAL PRIMARY KEY,
    account_code VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    sub_type VARCHAR(50),
    parent_code VARCHAR(20),
    description TEXT,
    normal_balance VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    is_header BOOLEAN DEFAULT FALSE,
    currency VARCHAR(10) DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts_payable (
    id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    vendor_code VARCHAR(30),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    amount NUMERIC(14,2) NOT NULL,
    paid_amount NUMERIC(14,2) DEFAULT 0,
    balance NUMERIC(14,2) NOT NULL,
    category VARCHAR(50),
    payment_terms VARCHAR(50),
    status VARCHAR(30),
    currency VARCHAR(10) DEFAULT 'USD',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE accounts_receivable (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_code VARCHAR(30),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    amount NUMERIC(14,2) NOT NULL,
    received_amount NUMERIC(14,2) DEFAULT 0,
    balance NUMERIC(14,2) NOT NULL,
    category VARCHAR(50),
    payment_terms VARCHAR(50),
    status VARCHAR(30),
    currency VARCHAR(10) DEFAULT 'USD',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_expense (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    description TEXT,
    amount NUMERIC(14,2) NOT NULL,
    department VARCHAR(50),
    vendor VARCHAR(100),
    cost_center VARCHAR(50),
    approved_by VARCHAR(100),
    status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_operating_cost (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    fuel_oil NUMERIC(14,2) DEFAULT 0,
    salaries_flight_crew NUMERIC(14,2) DEFAULT 0,
    salaries_ground_staff NUMERIC(14,2) DEFAULT 0,
    maintenance_repair NUMERIC(14,2) DEFAULT 0,
    airport_landing_fees NUMERIC(14,2) DEFAULT 0,
    aircraft_lease_rent NUMERIC(14,2) DEFAULT 0,
    distribution_sales NUMERIC(14,2) DEFAULT 0,
    catering_inflight NUMERIC(14,2) DEFAULT 0,
    insurance_safety NUMERIC(14,2) DEFAULT 0,
    depreciation_amort NUMERIC(14,2) DEFAULT 0,
    other_operating NUMERIC(14,2) DEFAULT 0,
    total_operating_cost NUMERIC(14,2) NOT NULL,
    casm NUMERIC(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_revenue (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    passenger_mainline NUMERIC(14,2) DEFAULT 0,
    passenger_regional NUMERIC(14,2) DEFAULT 0,
    cargo_mail NUMERIC(14,2) DEFAULT 0,
    ancillary_bags NUMERIC(14,2) DEFAULT 0,
    ancillary_seats NUMERIC(14,2) DEFAULT 0,
    ancillary_wifi NUMERIC(14,2) DEFAULT 0,
    ancillary_other NUMERIC(14,2) DEFAULT 0,
    loyalty_program NUMERIC(14,2) DEFAULT 0,
    contract_carrier NUMERIC(14,2) DEFAULT 0,
    total_revenue NUMERIC(14,2) NOT NULL,
    load_factor NUMERIC(6,2),
    rasm NUMERIC(10,4),
    asm NUMERIC(14,2),
    rpm NUMERIC(14,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_profit (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    total_revenue NUMERIC(14,2) NOT NULL,
    total_operating_cost NUMERIC(14,2) NOT NULL,
    gross_profit NUMERIC(14,2) NOT NULL,
    non_operating_income NUMERIC(14,2) DEFAULT 0,
    non_operating_expense NUMERIC(14,2) DEFAULT 0,
    pre_tax_income NUMERIC(14,2) NOT NULL,
    tax_provision NUMERIC(14,2) DEFAULT 0,
    net_income NUMERIC(14,2) NOT NULL,
    operating_margin NUMERIC(8,4),
    net_margin NUMERIC(8,4),
    ebitda NUMERIC(14,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE general_ledger (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    account_code VARCHAR(20) NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    debit NUMERIC(14,2) DEFAULT 0,
    credit NUMERIC(14,2) DEFAULT 0,
    description TEXT,
    reference VARCHAR(50),
    journal_type VARCHAR(50),
    department VARCHAR(50),
    cost_center VARCHAR(50),
    fiscal_period VARCHAR(20),
    is_reconciled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profit_loss_statement (
    id SERIAL PRIMARY KEY,
    period VARCHAR(20) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    passenger_revenue NUMERIC(14,2) DEFAULT 0,
    cargo_revenue NUMERIC(14,2) DEFAULT 0,
    ancillary_revenue NUMERIC(14,2) DEFAULT 0,
    loyalty_revenue NUMERIC(14,2) DEFAULT 0,
    other_revenue NUMERIC(14,2) DEFAULT 0,
    total_revenue NUMERIC(14,2) NOT NULL,
    fuel_expense NUMERIC(14,2) DEFAULT 0,
    labor_expense NUMERIC(14,2) DEFAULT 0,
    maintenance_expense NUMERIC(14,2) DEFAULT 0,
    airport_expense NUMERIC(14,2) DEFAULT 0,
    lease_expense NUMERIC(14,2) DEFAULT 0,
    distribution_expense NUMERIC(14,2) DEFAULT 0,
    catering_expense NUMERIC(14,2) DEFAULT 0,
    insurance_expense NUMERIC(14,2) DEFAULT 0,
    depreciation_expense NUMERIC(14,2) DEFAULT 0,
    other_expense NUMERIC(14,2) DEFAULT 0,
    total_expenses NUMERIC(14,2) NOT NULL,
    operating_income NUMERIC(14,2) NOT NULL,
    interest_expense NUMERIC(14,2) DEFAULT 0,
    interest_income NUMERIC(14,2) DEFAULT 0,
    fuel_hedging_gain_loss NUMERIC(14,2) DEFAULT 0,
    pre_tax_income NUMERIC(14,2) NOT NULL,
    income_tax NUMERIC(14,2) DEFAULT 0,
    net_income NUMERIC(14,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE revenue_recognition (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    transaction_type VARCHAR(50),
    booking_date DATE NOT NULL,
    service_date DATE NOT NULL,
    recognition_date DATE NOT NULL,
    gross_amount NUMERIC(14,2) NOT NULL,
    recognized_amount NUMERIC(14,2) DEFAULT 0,
    deferred_amount NUMERIC(14,2) DEFAULT 0,
    recognition_method VARCHAR(50),
    performance_obligation VARCHAR(100),
    status VARCHAR(30),
    flight_number VARCHAR(20),
    route VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT * FROM revenue_recognition