/*
  # Create history table

  1. New Tables
    - `history`
      - `id` (uuid, primary key)
      - `action_type` (text, check constraint for valid values)
      - `item_name` (text)
      - `quantity` (integer)
      - `obra` (text)
      - `n_factura` (text)
      - `warehouse_name` (text)
      - `user_name` (text)
      - `action_date` (timestamptz, default now)
      - `notes` (text, optional)
      - `item_id` (uuid, foreign key to items, nullable)
      - `user_id` (uuid, foreign key to users, nullable)
      - `warehouse_id` (uuid, foreign key to warehouses, nullable)
      - `created_at` (timestamptz, default now)
      - `updated_at` (timestamptz, default now)

  2. Security
    - Enable RLS on `history` table
    - Add policies for reading and creating history records

  3. Indexes
    - Create indexes for better query performance on common searches
*/

CREATE TABLE IF NOT EXISTS history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  action_type text NOT NULL CHECK (action_type IN ('withdrawal', 'addition', 'adjustment')),
  item_name text NOT NULL,
  quantity integer NOT NULL,
  obra text NOT NULL,
  n_factura text NOT NULL,
  warehouse_name text NOT NULL,
  user_name text NOT NULL,
  action_date timestamptz DEFAULT now(),
  notes text,
  item_id uuid REFERENCES items(id) ON DELETE SET NULL,
  user_id uuid REFERENCES users(id) ON DELETE SET NULL,
  warehouse_id uuid REFERENCES warehouses(id) ON DELETE SET NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_history_action_date ON history(action_date DESC);
CREATE INDEX IF NOT EXISTS idx_history_warehouse_id ON history(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_history_item_id ON history(item_id);
CREATE INDEX IF NOT EXISTS idx_history_user_id ON history(user_id);
CREATE INDEX IF NOT EXISTS idx_history_action_type ON history(action_type);
CREATE INDEX IF NOT EXISTS idx_history_obra ON history(obra);

-- Enable RLS
ALTER TABLE history ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist and recreate them
DO $$ 
BEGIN
  -- Drop existing policies
  DROP POLICY IF EXISTS "Users can read history" ON history;
  DROP POLICY IF EXISTS "System can create history records" ON history;
  
  -- Create policies
  CREATE POLICY "Users can read history"
    ON history
    FOR SELECT
    TO authenticated
    USING (true);

  CREATE POLICY "System can create history records"
    ON history
    FOR INSERT
    TO authenticated
    WITH CHECK (true);
END $$;

-- Create trigger if it doesn't exist
DROP TRIGGER IF EXISTS update_history_updated_at ON history;
CREATE TRIGGER update_history_updated_at
  BEFORE UPDATE ON history
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();