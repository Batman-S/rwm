import WaitlistForm from "./WaitlistForm";
const Home = () => {
  return (
    <div className="container mx-auto p-12 flex items-center justify-center ">
      <WaitlistForm
        onSubmit={(party) => {
          console.log("submit");
        }}
      />
    </div>
  );
};

export default Home;
