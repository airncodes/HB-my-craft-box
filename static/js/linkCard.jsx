function LinkCard(props) {
  return (
    <div className="card">
      <img src={props.image} alt="Image not available"/>
      <p><a href="{props.link_path}">{props.name}</a></p>
      <p> Notes: {props.notes} </p>
    </div>
    );
}

function LinkCardContainer() {
  const [cards, setCards] = React.useState([]);

  function addCard() {
    
    const currentCards = [...cards]; // makes a copy of cards. similar to doing currentCards = cards[:] in Python
    setCards([...currentCards]);
  }
    
  React.useEffect(() => {
    fetch('/craftbox.json')
      .then(response => response.json())
      .then(data => setCards(data.cards));
  }, []);

  const linkCards = [];

  console.log(`cards: `, cards);

  for (const currentCard of cards) {
    linkCards.push(
      <LinkCard
      // const newCard = {image, link_path, name, notes};
        image={currentCard.image}
        link_path={currentCard.link_path}
        name={currentCard.name}
        notes={currentCard.notes}
      />
    );
  }
  return (
    <React.Fragment>
      <linkCards addCard={addCard} />
      <h2>Links</h2>
      <div className="grid">{linkCards}</div>
    </React.Fragment>
  );
}


ReactDOM.render(<LinkCardContainer/>, document.querySelector('#linkcontainer'));
