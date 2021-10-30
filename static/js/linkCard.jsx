// Link card function to create a card of the link(s) added.

function LinkCard(props) {
  const [isModalVisible, setIsModalVisible] = React.useState(false);
  return (
    <div className="card">
      <img src={props.image} alt="Image not available"/>
      <p><a href={props.link_path}>{props.name}</a></p>
      <p className="notes"> Notes: {props.notes} </p>
      <button onClick={() => setIsModalVisible(true)}>Edit</button>
      {isModalVisible && (
        <Modal onModalClose={() => {setIsModalVisible(false), window.location.reload()}}>
          <Modal.Header>Edit {props.name} Card -{props.link_id}
          </Modal.Header>
          <Modal.Form link_id={props.link_id}>Options</Modal.Form>
          <Modal.Footer>
            <Modal.Footer.CloseBtn>Close</Modal.Footer.CloseBtn>
          </Modal.Footer>
        </Modal>
      )}
    </div>
    );
}
// More modal functions for editing the link cards.
const modalContext = React.createContext();

function Modal({ children, onModalClose }) {
  React.useEffect(() => {
    function keyListener(e) {
      const listener = keyListenersMap.get(e.keyCode);
      return listener && listener(e);
    }
    document.addEventListener("keydown", keyListener);

    return () => document.removeEventListener("keydown", keyListener);
  });

  const modalRef = React.createRef();
  const handleTabKey = e => {
    const focusableModalElements = modalRef.current.querySelectorAll(
      'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
    );
    const firstElement = focusableModalElements[0];
    const lastElement =
      focusableModalElements[focusableModalElements.length - 1];

    if (!e.shiftKey && document.activeElement !== firstElement) {
      firstElement.focus();
      return e.preventDefault();
    }

    if (e.shiftKey && document.activeElement !== lastElement) {
      lastElement.focus();
      e.preventDefault();
    }
  };

  const keyListenersMap = new Map([[27, onModalClose], [9, handleTabKey]]);

  return ReactDOM.createPortal(
    <div className="modal-container" role="dialog" aria-modal="true">
      <div className="modal-content" ref={modalRef}>
        <modalContext.Provider value={{ onModalClose }}>
          {children}
        </modalContext.Provider>
      </div>
    </div>,
    document.body
  );
}

Modal.Header = function ModalHeader(props) {
  const { onModalClose } = React.useContext(modalContext);

  return (
    <div className="modal-header">
      <h3>{props.children}</h3>
      <button className="cross-btn" title="close modal" onClick={onModalClose}>
        ✕
      </button>
    </div>
  );
};

Modal.Form = function ModalForm(props) {
  const [name, setName] = React.useState('');
  const [image, setImage] = React.useState('');
  const [notes, setNotes] = React.useState('');
  const link_id = props.link_id;
  // console.log(props.link_id);


  function editCard() {
    fetch('/edit-card', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({link_id, name, image, notes}),
    }).then(response => {
      console.log(response)
    });
  }

  function delCard() {
    fetch('/del-card', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({link_id}),
    }).then(response => {
      console.log(response)
    });
  }
  
  
  return (
    <React.Fragment>
    <label htmlFor="nameInput" style={{marginLeft: '10px'}}>
      Name
      <input className="modal-input" value={name} onChange={event => setName(event.target.value)} id="nameInput"/>
    </label>
    <br />
    <label htmlFor="imageInput" style={{marginLeft: '10px'}}>
      Image
      <input className="modal-input" value={image} onChange={event => setImage(event.target.value)} id="imageInput" />
    </label>
    <br />
    <label htmlFor="notesInput" style={{marginLeft: '10px'}}>
      Notes
      <input className="modal-input" value={notes} onChange={event => setNotes(event.target.value)} id="notesInput" />
    </label>
    <br />
    <input className="modal-input" type="number" name="link_id" defaultValue={props.link_id} hidden></input>
    <button className="submit-btn" onClick={editCard}>
      Make Change
    </button>
    <button className="del-btn" onClick={delCard}>
      Delete
    </button>
  </React.Fragment>);
};

Modal.Footer = function ModalFooter(props) {
  return <div className="modal-footer">{props.children}</div>;
};

Modal.Footer.CloseBtn = function CloseBtn(props) {
  const { onModalClose } = React.useContext(modalContext);
  return (
    <button
      {...props}
      className="close-btn"
      title="close modal"
      onClick={onModalClose}
    />
  );
};

// Creating the container of Link cards
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
      // const newCard = {link_id, image, link_path, name, notes};
        link_id={currentCard.link_id}
        image={currentCard.image}
        link_path={currentCard.link_path}
        name={currentCard.name}
        notes={currentCard.notes}
      />
    );
  }
  return (
    <React.Fragment>
      <h2>All Links</h2>
      <div className="grid">{linkCards}</div>
    </React.Fragment>
  );
}


ReactDOM.render(<LinkCardContainer/>, document.querySelector('#linkcontainer'));
