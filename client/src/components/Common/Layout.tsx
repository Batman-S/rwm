import Header from "./Header";
const Layout = ({ children }: React.PropsWithChildren) => {
  return (
    <div>
      <Header />
      <main className="h-full w-full container mx-auto p-12 flex items-center justify-center mt-8 bg-purple-secondary/10 rounded-md shadow-md">
        {children}
      </main>
    </div>
  );
};

export default Layout;
