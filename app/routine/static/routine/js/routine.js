const app = Vue.createApp({
    template: `
    <div id="data_center">
        <h1 class="routineTitle=">{{ updateWorkOnTitle }}</h1>
        <div class="work-pallet">
            <yrap-work-pallet-workout v-if="curWorkChoice === 'workout'">
            </yrap-work-pallet-workout>

            <yrap-work-pallet-bookReading v-if="curWorkChoice === 'bookReading'">
            </yrap-work-pallet-bookReading>

            <yrap-work-pallet-studying v-if="curWorkChoice === 'studying'">
            </yrap-work-pallet-studying>

            <yrap-work-pallet-routines v-if="curWorkChoice === 'routines'">
            </yrap-work-pallet-routines>

            <yrap-work-pallet-justDoIt v-if="curWorkChoice === 'justDoIt'">
            </yrap-work-pallet-justDoIt>
        </div>
    </div>

    <div id='commands'>
        <h2>Command</h2>

        <choose-what-to-work-on @updateWorkOn="nowWorkOn($event)"></choose-what-to-work-on>
        <pomodoro-timer></pomodoro-timer>
    </div>
    `,
    components: ['choose-what-to-work-on'],
    data() {
        return {
            updateWorkOnTitle: 'Manage and Track your routines',
            curWorkChoice: null
        }
    },
    methods: {
        updateTitle(title) {
            const workChoices = {
                workout: 'Workout',
                bookReading: 'Book Reading',
                studying: 'Studying',
                routines: 'Routines',
                justDoIt: 'Just Do It Items',

            };
            this.updateWorkOnTitle = "Manage and track: " + workChoices[title];

        },
        nowWorkOn(value) {
            // Update the page title
            this.updateTitle(value);
            // Set the page data
            this.curWorkChoice = value;
        }
    }
})
app.component('yrap-work-pallet-workout', {
    template: `
    <div class='work-pallet-container'>
    yrap-work-pallet-workout
    </div>
    `
})
app.component('yrap-work-pallet-bookReading', {
    template: `
    <div class='work-pallet-container'>
    yrap-work-pallet-bookReading
    </div>
    `
})
app.component('yrap-work-pallet-studying', {
    template: `
    <div class='work-pallet-container'>
        <h3>{{ studyBlockTitle }}</h3>
        <form @submit.prevent="genStudyChoice">
            <div class='limitLength'>
                <div v-if="studyItems.length" :key="makeUpdateKey">
                    <div v-for="studyItem in studyItems" :key="studyItem">
                        <button class='btn-manage' :name="studyItem.reference">{{ studyItem.goal }}</button>
                    </div>
                </div>
                <span v-else>
                    <p>No items retrieved....</p>
                </span>
                <div><button name='add-new' class='btn-manage'>Add a new study item</button></div>
            </div>
        </form>
        <span v-if="showAddNewItemForm">
            <add-new-study-item-form @closeChildPopUp="closeChildPopUpNow"></add-new-study-item-form>
        </span>
        <span v-if="showWorkOnStudyItem">
            <work-on-study-item-page @closeChildPopUp="closeChildPopUpNow" :studyItemData='curStudyItem'></work-on-study-item-page>
        </span>
    </div>
    `,
    components: ['add-new-study-item-form', 'work-on-study-item-page'],
    data() {
        return {
            studyBlockTitle: "Choose what to work on",
            studyItems: [],
            showAddNewItemForm: false,
            showWorkOnStudyItem: false,
            curStudyItem: [],
            makeUpdateKey: 0
        }
    },
    mounted() {
        this.fetchstudyChoices();
    },
    methods: {
        async fetchstudyChoices() {
            await fetch('/routine/api/studychunkscorecard/')
                .then(res => res.json())
                .then(data => this.studyItems = data)
                .catch(err => console.log(err.message))
        },
        genStudyChoice() {
            const studyChoiceItem = document.activeElement.getAttribute('name');
            if (studyChoiceItem === 'add-new') {
                this.showAddNewItemForm = true;
            } else {
                const curStudyItem = this.studyItems.find(a => a.reference === studyChoiceItem);
                this.showWorkOnStudyItem = true;
                this.curStudyItem = curStudyItem;
            }
        },
        async closeChildPopUpNow() {
            this.showAddNewItemForm = false;
            this.showWorkOnStudyItem = false;
            await this.fetchstudyChoices();
            this.makeUpdateKey += 1;
        }
    }
})
app.component('work-on-study-item-page', {
    template: `
        <div class='work-on-study-item-page'>
            <div class='work-on-study-item-page-inner'>
                <div class='manage-work-study'>
                    <h1>Project Goal: {{ studyItemData.goal }}</h1>
                    <div v-if="todayValues.got_data">
                        <p>Today's target: {{ todayValues.target }}</p>

                        <form @submit.prevent="updateAchieved">
                        <label for='achieved-input'>Enter the page/lesson you end on today</label>
                        <input id="achieved-input" @keyup.enter.prevent="updateAchieved" name='achieved-input' type='text' :placeholder=todayValues.achieved class='achieved-input-field' required>
                        <button class='submit'>Submit</button>
                        </form>
                    </div>
                    <div v-else>
                        <p>This study item starts {{ startDate }}</p>
                    </div>

                </div>
                <div class='manage-work-study'>
                    <img class='graph-image' :src="todayValues.graph" alt='study progress graph' :key="updateGraphKey">
                </div>

                <button @click.prevent="closePopUp" class='close-pop-up' name='close'>&times;</button>
            </div>
        </div>
    `,
    data() {
        return {
            someValue: '',
            itemData: this.studyItemData,
            todayValues: [],
            achieved: 0,
            startDate: '',
            updateGraphKey: 0
        }
    },
    mounted() {
        this.fetchData();
        const startDate = new Date(this.studyItemData.start_date);
        this.startDate = startDate.toLocaleDateString();
    },
    props: ['studyItemData'],
    methods: {
        async updateAchieved() {
            const achieved_input = document.querySelector('#achieved-input').value;
            const requestOptions = {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': $.cookie('csrftoken')
                }
            };
            await fetch('/routine/api/studychunkscorecard_achieved/' + this.studyItemData.id + '/' + achieved_input + '/', requestOptions)
                .then(response => response.json())
                .then(data => data_update = data)
                .catch(err => console.log(err.message))
            this.todayValues.achieved = achieved_input;
            this.todayValues.graph = data_update.graph;
            this.updateGraphKey += 1;
            this.todayValues.graph = this.todayValues.graph + "?update=" + this.updateGraphKey;
        },
        async fetchData() {
            await fetch('/routine/api/studychunkscorecard_workon/' + this.itemData.id + '/' + this.itemData.reference + '/')
                .then(response => response.json())
                .then(data => this.todayValues = data)
                .catch(err => console.log(err.message))
            this.achieved = this.todayValues.achieved;
        },
        closePopUp() {
            this.$emit('closeChildPopUp')
        }
    }

})
app.component('add-new-study-item-form', {
    template: `
    <div class='add-new-study-item-pop-up'>
        <div class='add-new-study-item-pop-up-inner'>
            <form @submit.prevent="submitItem">

                <label for="reference">Reference</label>
                <input type="text" name="reference" v-model='reference' required>

                <label for="goal">Goal/Title</label>
                <input type="text" name="goal" v-model='goal' required>

                <label for="authors">Authors</label>
                <input id="add_author_field" @focus.native="addAuthors" type="text" name="authors" autocomplete="off">

                <label for="start_date">Start Date</label>
                <input type="datetime-local" name="start_date" v-model='start_date' required>

                <label for="end_date">End Date</label>
                <input type="datetime-local" name="end_date" v-model='end_date' required>

                <label for="start_page">Start Page</label>
                <input type="number" name="start_page" required min="1" max="2000" v-model='start_page'>

                <label for="end_page">End Page</label>
                <input type="number" name="end_page" required min="1" max="2000" v-model='end_page'>

                <button @click.prevent="closePopUp" class='close-pop-up' name='close'>&times;</button>
                <button class='submit' name='submit'>Submit</button>
            </form>
            <span v-if="showAddAuthorsForm">
                <add-new-study-authors @closeAddAuthorPopUp="closeAddAuthorPopUpNow"></add-new-study-authors>
            </span>
        </div>
    </div>
    `,
    data() {
        return {
            reference: '',
            goal: '',
            authors: [],
            start_date: '',
            end_date: '',
            start_page: null,
            end_page: null,
            showAddAuthorsForm: false
        }
    },
    components: ['add-new-study-authors'],
    methods: {
        addAuthors() {
            this.showAddAuthorsForm = true
        },
        closeAddAuthorPopUpNow(authorValues) {
            this.authors = [];
            const authorField = document.querySelector('#add_author_field');
            let authorString = '';
            authorValues.forEach((author, index) => {
                authorString = authorString + author.first_name + ' ' + author.last_name
                this.authors.push(author.id);
                if (authorValues.length - 1 !== index) {
                    authorString += '; ';
                }
            });
            authorField.value = authorString;
            this.showAddAuthorsForm = false
        },
        closePopUp() {
            this.$emit('closeChildPopUp')
        },
        async submitItem() {
            const doSubmission = document.activeElement.getAttribute('name');
            if (doSubmission === 'submit') {
                let newStudyItem = {};
                newStudyItem['reference'] = this.reference
                newStudyItem['goal'] = this.goal
                newStudyItem['authors'] = this.authors
                let start_date = new Date(this.start_date);
                newStudyItem['start_date'] = start_date.toISOString();
                let end_date = new Date(this.end_date);
                newStudyItem['end_date'] = end_date.toISOString()
                newStudyItem['start_page'] = this.start_page
                newStudyItem['end_page'] = this.end_page

                const requestOptions = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': $.cookie('csrftoken')
                    },
                    body: JSON.stringify(newStudyItem)
                };
                await fetch('/routine/api/studychunkscorecard/', requestOptions)
                    .then(response => response.json())
                    .then(data => this.author = data)
                    .catch(err => console.log(err.message))

            }
            this.closePopUp();
        }
    }
})
app.component('add-new-study-authors', {
    template: `
        <div class='add-new-study-authors-pop-up'>

        <form @submit.prevent="submitAuthors">
            <div class='limitLength'>
                <span v-if="authors.length">
                    <div v-for="author in makeAuthors" :key="author">
                        <label :for='author.id' class='container'>{{ author.first_name }} {{ author.last_name }}
                            <button class="no-tick-mark" :name="author.id"></button>
                            <button class="tick-mark" :name="author.id"></button>
                        </label>
                    </div>
                </span>
            </div>
            <button class='submit'>Add These Authors</button>
        </form>

        <h3>Add another author</h3>
        <form @submit.prevent="createAuthor">
            <label for='first_name'>First Name</label>
            <input type='text' name='first_name' v-model='first_name' class='new-author-input-field' required>
            <label for='last_name'>Last Name</label>
            <input type='text' name='last_name' v-model='last_name' class='new-author-input-field' required>
            <button class='submit'>Add New Author</button>
        </form>

        <button @click.prevent="closeAuthorPopUp(false)" class='close-pop-up' name='close'>&times;</button>
        </div>
    `,
    data() {
        return {
            authors: [],
            first_name: '',
            last_name: '',
            selectedAuthorIDs: [],
            outputAuthors: []
        }
    },
    computed: {
        makeAuthors() {
            return this.authors;
        }
    },
    mounted() {
        this.fetchAuthors()
    },
    methods: {
        async createAuthor() {
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                body: JSON.stringify({ first_name: this.first_name, last_name: this.last_name })
            };
            await fetch('/routine/api/authors/', requestOptions)
                .then(response => response.json())
                .then(data => this.author = data)
                .catch(err => console.log(err.message))
            this.fetchAuthors()
            this.first_name = ''
            this.last_name = ''
        },
        async fetchAuthors() {
            await fetch('/routine/api/authors/')
                .then(res => res.json())
                .then(data => this.authors = data)
                .catch(err => console.log(err.message))
        },
        closeAuthorPopUp(sendAuthors) {
            let output = []
            if (sendAuthors) {
                output = this.outputAuthors
            }
            this.$emit('closeAddAuthorPopUp', output);
        },
        submitAuthors() {
            // read the authors, set the values, and close the window;
            const pressedButton = document.activeElement;
            const whichButton = pressedButton.getAttribute('name');
            if (pressedButton.getAttribute('class') === 'no-tick-mark') {
                pressedButton.style.display = 'none';
                this.outputAuthors.push(this.authors.find(a => a.id === parseInt(whichButton)));
                let tickButtons = document.querySelectorAll('.tick-mark');
                for (let i = 0; i < tickButtons.length; i++) {
                    if (tickButtons[i].getAttribute('name') === whichButton) {
                        tickButtons[i].style.display = 'inline-block';
                        break;
                    }
                }
            } else if (pressedButton.getAttribute('class') === 'tick-mark') {
                const index = this.outputAuthors.indexOf(this.authors.find(a => a.id === parseInt(whichButton)));
                if (index > -1) {
                    this.outputAuthors.splice(index, 1);
                }
                pressedButton.style.display = 'none';
                let tickButtons = document.querySelectorAll('.no-tick-mark');
                for (let i = 0; i < tickButtons.length; i++) {
                    if (tickButtons[i].getAttribute('name') === whichButton) {
                        tickButtons[i].style.display = 'inline-block';
                        break;
                    }
                }
            } else {
                this.closeAuthorPopUp(true);
            }
        }
    }
})
app.component('yrap-work-pallet-routines', {
    template: `
        <div class='work-pallet-container'>yrap-work-pallet-routines</div>
    `
})
app.component('yrap-work-pallet-justDoIt', {
    template: `
        <div class='work-pallet-container'>
            <div v-if="justDoIts.length">
                <div v-for="justDoIt in justDoIts" class='just_do_it_items' :key="justDoIt">
                    <label :for="justDoIt.name">{{ justDoIt.description }}:
                    <input type="checkbox" :name="justDoIt.name" value="{{ justDoIt.checked }}" v-model="justDoIt.checked">
                    </label>
                </div>
            </div>
            <div v-else>
                <p>No "Just Do It" items exist yet</p>
            </div>

            <form @submit.prevent="addJustDoIt">
                <button>Add</button>
            </form>
        
        </div>
    `,
    data() {
        return {
            justDoIts: []
        }
    },
    mounted() {
        this.getJustDoIts();
    },
    updated() {
        this.checkJustDoItDay()
    },
    methods: {
        async addJustDoIt() {
            console.log('TODO: add new just do it')
        },
        async checkJustDoItDay() {
            const requestOptions = {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': $.cookie('csrftoken')
                },
                body: JSON.stringify(this.justDoIts)
            };
            await fetch('/routine/api/justdoit/checked/', requestOptions)
                .catch(err => console.log(err.message))
        },
        async getJustDoIts() {
            await fetch('/routine/api/justdoit/')
                .then(response => response.json())
                .then(data => this.justDoIts = data)
                .catch(err => console.log(err.message))
            for (let i = 0; i < this.justDoIts.length; i++) {
                this.justDoIts[i]['name'] = this.justDoIts[i].description + '_' + this.justDoIts[i].id;
            }
            this.getJustDoTodays();
            await fetch('/routine/api/justdoit/checked/')
                .then(response => response.json())
                .then(data => checkedItems = data)
                .catch(err => console.log(err.message))
                // for (let i = 0; i < checkedItems.length; i++) {
                //     let id = checkedItems[i]['id'];
            for (const item in checkedItems) {
                let id = checkedItems[item]['id'];
                for (let j = 0; j < this.justDoIts.length; j++) {
                    if (this.justDoIts[j]['id'] === id) {
                        this.justDoIts[j]['checked'] = checkedItems[item].checked;
                        break;
                    }
                }
            }
        },
        async getJustDoTodays() {
            let justDoTodays = [];
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': $.cookie('csrftoken')
                }
            };
            await fetch('/routine/api/justdoit/make_today/', requestOptions)
                .then(response => response.json())
                .then(data => justDoTodays = data)
                .catch(err => console.log(err.message))
            for (let i = 0; i < justDoTodays.length; i++) {
                let id = justDoTodays[i].id;
                for (let j = 0; j < this.justDoIts.length; j++) {
                    if (this.justDoIts[i]['id'] === id) {
                        this.justDoIts[i]['checked'] = justDoTodays[i]['checked'];
                    }
                }
            }

        }
    }
})
app.component('choose-what-to-work-on', {
    // Manage the type of content being worked on through buttons
    template: `
        <div class="btn-group">
            <form @submit.prevent="genWorkChoice">
                <button v-for="button in buttons" :key="button" :name=button.name>{{ button.value }}</button>
            </form>
        </div>
            `,
    data() {
        return {
            buttons: [{
                    name: "workout",
                    value: "Workouts"
                },
                {
                    name: "bookReading",
                    value: "Book Reading"

                },
                {
                    name: "studying",
                    value: "Studying"

                },
                {
                    name: "routines",
                    value: "Routines"

                },
                {
                    name: "justDoIt",
                    value: "Just Do It Items"

                }
            ]
        }
    },
    methods: {
        genWorkChoice(event) {
            const workonItem = document.activeElement.getAttribute('name');
            this.$emit('updateWorkOn', workonItem)
        }
    }
})
app.component('pomodoro-timer', {
    // Manage the pomodoro timer
    template: ` 
    <div class='pomodoro-container'>
        <button class='pomodoro-element start'>Start</button>
        <button class='pomodoro-element stop'>Stop</button>
        <button class='pomodoro-element pause'>Pause</button>
        <button class='pomodoro-element reset'>Reset</button>
        <div class='pomodoro-element pomodoro-element-timer'>
        <span class='pomodoro-inner-element pomodoro-minutes'>00</span>
        <span class='pomodoro-inner-element'>:</span>
        <span class='pomodoro-inner-element pomodoro-seconds'>00</span>
        </div>
    </div>
            `,
})
app.mount('#app')