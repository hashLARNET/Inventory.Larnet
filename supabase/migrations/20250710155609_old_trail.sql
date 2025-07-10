/*
  # Insert initial data

  1. Initial Users
    - Admin_Santiago (admin)
    - Operador_Juan (regular user)
    - Operador_Maria (regular user)
    - Supervisor_Carlos (regular user)

  2. Initial Warehouses
    - Bodega Principal
    - Bodega Secundaria
    - Bodega Herramientas

  3. Sample Items
    - Various construction tools and materials
*/

-- Insert initial users (passwords are hashed with bcrypt)
-- Note: In production, these should be created through your application's user registration
INSERT INTO users (username, hashed_password, full_name, is_admin, is_active) VALUES
  ('Admin_Santiago', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/SJHSBxoxe', 'Administrador Santiago', true, true),
  ('Operador_Juan', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/SJHSBxoxe', 'Juan Pérez', false, true),
  ('Operador_Maria', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/SJHSBxoxe', 'María González', false, true),
  ('Supervisor_Carlos', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/SJHSBxoxe', 'Carlos Rodríguez', false, true)
ON CONFLICT (username) DO NOTHING;

-- Insert initial warehouses
INSERT INTO warehouses (name, code, description, location, is_active) VALUES
  ('Bodega Principal', 'BP001', 'Bodega principal del almacén', 'Edificio A - Piso 1', true),
  ('Bodega Secundaria', 'BS002', 'Bodega secundaria para overflow', 'Edificio B - Piso 2', true),
  ('Bodega Herramientas', 'BH003', 'Bodega especializada en herramientas', 'Edificio A - Piso 2', true)
ON CONFLICT (code) DO NOTHING;

-- Insert sample items
-- Note: We'll use the warehouse IDs from the inserted warehouses
DO $$
DECLARE
  warehouse_bp uuid;
  warehouse_bs uuid;
  warehouse_bh uuid;
BEGIN
  -- Get warehouse IDs
  SELECT id INTO warehouse_bp FROM warehouses WHERE code = 'BP001';
  SELECT id INTO warehouse_bs FROM warehouses WHERE code = 'BS002';
  SELECT id INTO warehouse_bh FROM warehouses WHERE code = 'BH003';

  -- Insert sample items
  INSERT INTO items (name, description, barcode, stock, unit_price, obra, n_factura, warehouse_id) VALUES
    ('Martillo', 'Martillo de acero 500g', '7501234567890', 25, 15.50, 'Construcción Casa A', 'FAC-001', warehouse_bh),
    ('Destornillador Phillips', 'Destornillador Phillips #2', '7501234567891', 50, 8.75, 'Construcción Casa A', 'FAC-001', warehouse_bh),
    ('Taladro Eléctrico', 'Taladro eléctrico 600W', '7501234567892', 8, 125.00, 'Construcción Casa B', 'FAC-002', warehouse_bh),
    ('Tornillos', 'Tornillos autorroscantes 3x25mm (caja 100)', '7501234567893', 200, 12.30, 'Construcción Casa A', 'FAC-001', warehouse_bp),
    ('Sierra Manual', 'Sierra manual para madera 20"', '7501234567894', 15, 22.50, 'Construcción Casa C', 'FAC-003', warehouse_bh),
    ('Nivel de Burbuja', 'Nivel de burbuja 60cm', '7501234567895', 12, 18.90, 'Construcción Casa B', 'FAC-002', warehouse_bh),
    ('Cinta Métrica', 'Cinta métrica 5m', '7501234567896', 30, 9.25, 'Construcción Casa A', 'FAC-001', warehouse_bp),
    ('Alicate', 'Alicate universal 8"', '7501234567897', 20, 14.75, 'Construcción Casa C', 'FAC-003', warehouse_bh),
    ('Llave Inglesa', 'Llave inglesa ajustable 10"', '7501234567898', 18, 16.80, 'Construcción Casa B', 'FAC-002', warehouse_bs),
    ('Soldadora', 'Soldadora eléctrica 200A', '7501234567899', 3, 450.00, 'Construcción Casa C', 'FAC-003', warehouse_bh)
  ON CONFLICT (barcode) DO NOTHING;
END $$;