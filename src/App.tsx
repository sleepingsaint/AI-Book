import Layout from "components/Layout";
import { ResourceContextProvider } from "contexts/ResourceContext";
import { QueryClient, QueryClientProvider } from "react-query";
import LayoutTest from "ui_testing/LayoutTest";

const queryClient = new QueryClient();

function App() {
  return (
    <div className="App">
      <QueryClientProvider client={queryClient}>
        <ResourceContextProvider>
          <Layout />
          {/* <LayoutTest /> */}
        </ResourceContextProvider>
      </QueryClientProvider>
    </div>
  );
}

export default App;
