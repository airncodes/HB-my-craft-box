// Link card function to create a card of the link(s) added.
function LinkCard(props) {
  const [isModalVisible, setIsModalVisible] = React.useState(false);
  return (
    <div className="card">
      <img src={props.image} alt="Image not available"/>
      <p><a href="{props.link_path}">{props.name}</a></p>
      <p> Notes: {props.notes} </p>
      <button onClick={() => setIsModalVisible(true)}>Edit</button>
      {isModalVisible && (
        <Modal onModalClose={() => setIsModalVisible(false)}>
          <Modal.Header>Edit Card</Modal.Header>
          <Modal.Body>Body</Modal.Body>
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
      {props.children}
      <button className="cross-btn" title="close modal" onClick={onModalClose}>
        ✕
      </button>
    </div>
  );
};

Modal.Body = function ModalBody(props) {
  return <div className="modal-body">{props.children}</div>;
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
