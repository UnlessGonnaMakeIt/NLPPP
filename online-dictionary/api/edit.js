import { MongoClient, ObjectId } from 'mongodb';

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const { english, chinese } = req.body;
        const entryId = req.query.id;

        try {
            await client.connect();
            const db = client.db('dictionary');
            const collection = db.collection('entries');
            await collection.updateOne(
                { _id: new ObjectId(entryId) },
                { $set: { english, chinese } }
            );

            res.status(200).json({ message: 'Entry updated successfully!' });
        } finally {
            await client.close();
        }
    } else {
        res.status(405).json({ message: 'Method not allowed' });
    }
}