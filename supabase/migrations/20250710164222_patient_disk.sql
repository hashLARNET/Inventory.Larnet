/*
  # Create withdrawals and withdrawal_items tables

  1. New Tables
    - `withdrawals`
      - `id` (uuid, primary key)
      - `withdrawal_date` (timestamptz, default now)
      - `obra` (text)
      - `notes` (text, optional)
      - `user_id` (uuid, foreign key to users)
      - `warehouse_id` (uuid, foreign key to warehouses)
      - `created_at` (timestamptz, default now)
      - `updated_at` (timestamptz, default now)
    
    - `withdrawal_items`
      - `id` (uuid, primary key)
      - `quantity` (integer)
      - `withdrawal_id` (uuid, foreign key to withdrawals)
      - `item_id` (uuid, foreign key to items)
      - `created_at` (timestamptz, default now)
      - `updated_at` (timestamptz, default now)

  2. Security
    - Enable RLS on both tables
    - Add policies for reading and creating withdrawals
    - Add policies for reading and creating withdrawal items

  3. Indexes
    - Create indexes for better query performance
*/

CREATE TABLE IF NOT EXISTS withdrawals (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  withdrawal_date timestamptz DEFAULT now(),
  obra text NOT NULL,
  notes text,
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  warehouse_id uuid NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS withdrawal_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  quantity integer NOT NULL,
  withdrawal_id uuid NOT NULL REFERENCES withdrawals(id) ON DELETE CASCADE,
  item_id uuid NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_withdrawals_user_id ON withdrawals(user_id);
CREATE INDEX IF NOT EXISTS idx_withdrawals_warehouse_id ON withdrawals(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_withdrawals_obra ON withdrawals(obra);
CREATE INDEX IF NOT EXISTS idx_withdrawal_items_withdrawal_id ON withdrawal_items(withdrawal_id);
CREATE INDEX IF NOT EXISTS idx_withdrawal_items_item_id ON withdrawal_items(item_id);

-- Enable RLS
ALTER TABLE withdrawals ENABLE ROW LEVEL SECURITY;
ALTER TABLE withdrawal_items ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist and recreate them
DO $$ 
BEGIN
  -- Drop existing policies for withdrawals
  DROP POLICY IF EXISTS "Users can read withdrawals" ON withdrawals;
  DROP POLICY IF EXISTS "Users can create withdrawals" ON withdrawals;
  
  -- Drop existing policies for withdrawal_items
  DROP POLICY IF EXISTS "Users can read withdrawal items" ON withdrawal_items;
  DROP POLICY IF EXISTS "Users can create withdrawal items" ON withdrawal_items;
  
  -- Create policies for withdrawals
  CREATE POLICY "Users can read withdrawals"
    ON withdrawals
    FOR SELECT
    TO authenticated
    USING (true);

  CREATE POLICY "Users can create withdrawals"
    ON withdrawals
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

  -- Create policies for withdrawal_items
  CREATE POLICY "Users can read withdrawal items"
    ON withdrawal_items
    FOR SELECT
    TO authenticated
    USING (true);

  CREATE POLICY "Users can create withdrawal items"
    ON withdrawal_items
    FOR INSERT
    TO authenticated
    WITH CHECK (
      EXISTS (
        SELECT 1 FROM withdrawals 
        WHERE id = withdrawal_id AND user_id = auth.uid()
      )
    );
END $$;

-- Create triggers if they don't exist
DROP TRIGGER IF EXISTS update_withdrawals_updated_at ON withdrawals;
CREATE TRIGGER update_withdrawals_updated_at
  BEFORE UPDATE ON withdrawals
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_withdrawal_items_updated_at ON withdrawal_items;
CREATE TRIGGER update_withdrawal_items_updated_at
  BEFORE UPDATE ON withdrawal_items
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();