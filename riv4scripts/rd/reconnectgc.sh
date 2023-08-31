#!/bin/bash


echo "Connecting now."

# Airport 1
jack_connect rivendell_0:playout_0L stap1:input_1
jack_connect rivendell_0:playout_0R stap1:input_2


# Airport 2
jack_connect rivendell_0:playout_1L stap2:input_1
jack_connect rivendell_0:playout_1R stap2:input_2

# Airport 3
jack_connect rivendell_0:playout_2L stap3:input_1
jack_connect rivendell_0:playout_2R stap3:input_2

# Airport 4
jack_connect rivendell_0:playout_3L stap4:input_1
jack_connect rivendell_0:playout_3R stap4:input_2



