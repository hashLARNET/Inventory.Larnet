/*
  # Create withdrawals and withdrawal_items tables

  1. New Tables
    - `withdrawals`
      - `id` (uuid, primary key)
      - `withdrawal_date` (timestamp)
      - `obra` (text)
      - `notes` (text)
      - `user_id` (uuid, foreign key)
      - `warehouse_id` (uuid, foreign key)
      - `created_at` (timestamp)
      - `updated_at` (timestamp)
    
    - `withdrawal_items`
      - `id` (uuid, primary key)
      - `quantity` (integer)
      - `withdrawal_id` (uuid, foreign key)
      - `item_id` (uuid, foreign key)
      - `created_at` (timestamp)
      - `updated_at` (timestamp)

  2. Security
    - Enable RLS on both tables
    - Add policies for authenticated users to manage their withdrawals
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

-- Policies for withdrawals
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

-- Policies for withdrawal_items
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

-- Update triggers
CREATE TRIGGER update_withdrawals_updated_at
  BEFORE UPDATE ON withdrawals
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_withdrawal_items_updated_at
  BEFORE UPDATE ON withdrawal_items
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();