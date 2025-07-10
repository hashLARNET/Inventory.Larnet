/*
  # Create warehouses table

  1. New Tables
    - `warehouses`
      - `id` (uuid, primary key)
      - `name` (text, unique)
      - `code` (text, unique)
      - `description` (text, optional)
      - `location` (text, optional)
      - `is_active` (boolean, default true)
      - `created_at` (timestamptz, default now)
      - `updated_at` (timestamptz, default now)

  2. Security
    - Enable RLS on `warehouses` table
    - Add policy for users to read active warehouses
    - Add policy for admins to manage all warehouses
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

-- Drop existing policies if they exist and recreate them
DO $$ 
BEGIN
  -- Drop existing policies
  DROP POLICY IF EXISTS "Users can read active warehouses" ON warehouses;
  DROP POLICY IF EXISTS "Admins can manage warehouses" ON warehouses;
  
  -- Create policies
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
END $$;

-- Create trigger if it doesn't exist
DROP TRIGGER IF EXISTS update_warehouses_updated_at ON warehouses;
CREATE TRIGGER update_warehouses_updated_at
  BEFORE UPDATE ON warehouses
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();