async function getDoc(collection, doc) {
    let doc_data = {'null': true, 'id': null};
    await fetch(`https://voyager-api-pq2h.onrender.com/get/doc/${collection}/${doc}`)
		.then(response => response.json())
		.then(json => {
			doc_data = json;
		}).catch(error => console.error('Error:', error));

    return doc_data;
}

async function setDoc(collection, doc, data) {
    let doc_data = {'null': true, 'id': null};
    await fetch(`https://voyager-api-pq2h.onrender.com/set/doc/${collection}/${doc}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
		.then(response => response.json())
		.then(json => {
			doc_data = json;
		}).catch(error => console.error('Error:', error));

    return doc_data;
}

async function updateDoc(collection, doc, data) {
    let doc_data = {'null': true, 'id': null};
    await fetch(`https://voyager-api-pq2h.onrender.com/update/doc/${collection}/${doc}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
		.then(response => response.json())
		.then(json => {
			doc_data = json;
		}).catch(error => console.error('Error:', error));

    return doc_data;
}

async function getCollection(collection) {
    let doc_data = {'null': {'null': true, 'id': null}};
    await fetch(`https://voyager-api-pq2h.onrender.com/get/collection/${collection}`)
		.then(response => response.json())
		.then(json => {
			doc_data = json;
		}).catch(error => console.error('Error:', error));

    return doc_data;
}