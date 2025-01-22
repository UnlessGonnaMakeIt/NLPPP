import { MongoClient } from 'mongodb';

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

export default async function handler(req, res) {
    if (req.method === 'GET') {
        try {
            await client.connect();
            const db = client.db('dictionary');
            const collection = db.collection('entries');
            const personEntries = await collection.find({ category: 'person' }).toArray();
            const placeEntries = await collection.find({ category: 'place' }).toArray();
            const properEntries = await collection.find({ category: 'proper' }).toArray();

            res.status(200).json({ person: personEntries, place: placeEntries, proper: properEntries });
        } finally {
            await client.close();
        }
    } else {
        res.status(405).json({ message: 'Method not allowed' });
    }
}