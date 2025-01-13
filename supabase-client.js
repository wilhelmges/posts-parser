import { createClient } from '@supabase/supabase-js'
import * as dotenv from 'dotenv';
dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseKey)

const { data, error } = await supabase
    .from('test')
    .insert([
        { text: 'value1' },
    ])