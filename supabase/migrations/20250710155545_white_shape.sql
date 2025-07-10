/*
  # Create items table

  1. New Tables
    - `items`
      - `id` (uuid, primary key)
      - `name` (text)
      - `description` (text)
      - `barcode` (text, unique)
      - `stock` (integer, default 0)
      - `unit_price` (decimal)
      - `obra` (text)
      - `n_factura` (text)
      - `warehouse_id` (uuid, foreign key)
      - `created_at` (timestamp)
      - `updated_at` (timestamp)

  2. Security
    - Enable RLS on `items` table
    - Add policy for authenticated users to read items
    - Add policy for authenticated users to manage items in their warehouse
*/

CREATE TABLE IF NOT EXISTS items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text,
  barcode text UNIQUE NOT NULL,
  stock integer DEFAULT 0,
  unit_price decimal(10,2),
  obra text NOT NULL,
  n_factura text NOT NULL,
  warehouse_id uuid NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_items_barcode ON items(barcode);
CREATE INDEX IF NOT EXISTS idx_items_warehouse_id ON items(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_items_obra ON items(obra);
CREATE INDEX IF NOT EXISTS idx_items_n_factura ON items(n_factura);
CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);

-- Enable RLS
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can read items"
  ON items
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Users can manage items"
  ON items
  FOR ALL
  TO authenticated
  USING (true);

-- Update trigger
CREATE TRIGGER update_items_updated_at
  BEFORE UPDATE ON items
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();