import { createClient } from '@supabase/supabase-js'
import * as dotenv from 'dotenv';
dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_KEY
const supabaseClient = createClient(supabaseUrl, supabaseKey)

// const { data, error } = await supabase
//     .from('test')
//     .insert([
//         { text: 'value18' },
//     ])

const { data, error } = await supabaseClient
    .from('test')
    .select()

console.log(data)