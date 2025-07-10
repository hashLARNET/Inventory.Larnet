/*
  # Create warehouses table

  1. New Tables
    - `warehouses`
      - `id` (uuid, primary key)
      - `name` (text, unique)
      - `code` (text, unique)
      - `description` (text)
      - `location` (text)
      - `is_active` (boolean, default true)
      - `created_at` (timestamp)
      - `updated_at` (timestamp)

  2. Security
    - Enable RLS on `warehouses` table
    - Add policy for authenticated users to read active warehouses
    - Add policy for admins to manage warehouses
*/

CREATE TABLE IF NOT EXISTS warehouses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text UNIQUE NOT NULL,
  code text UNIQUE NOT NULL,
  description text,
  location text,
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE warehouses ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can read active warehouses"
  ON warehouses
  FOR SELECT
  TO authenticated
  USING (is_active = true);

CREATE POLICY "Admins can manage warehouses"
  ON warehouses
  FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE id = auth.uid() AND is_admin = true
    )
  );

-- Update trigger
CREATE TRIGGER update_warehouses_updated_at
  BEFORE UPDATE ON warehouses
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();