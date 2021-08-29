const plant_production = {template:'

<table class="table table-striped">
<thead>
    <tr>
        <th>
        Id
        </th>
        <th>
        Plant
        </th>
        <th>
        Operator name
        </th>
    </tr>
    <tbody>
        <tr v-for pro in plant_productions>
            <td>
                {{pro.id}}
            </td>
            <td>
                {{pro.plant}}
            </td>
            <td>
                {{pro.operator_name}}
            </td>
            <td>
                <button class="btn btn-success"></button>
            </td>
        </tr>

    </tbody
</thead>



</table>',
    data(){
        return{
            plant_productions = []

        }
    },
    methods:{
        refreshData(){
            axios.get(variables.API_URL+"production"){
                .then((response)=>{
                    this.plant_productions = response.data
                )};
            }
        },
    }
}